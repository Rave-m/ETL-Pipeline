import sys
import os
from unittest.mock import patch, MagicMock
import pandas as pd

# Add the project root to the path so we can import the utils package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.load import store_to_postgre

@patch('utils.load.create_engine')
def test_store_to_postgre(mock_create_engine):
    """Test storing data to PostgreSQL"""
    # Create mock engine and connection
    mock_engine = MagicMock()
    mock_conn = MagicMock()
    mock_create_engine.return_value = mock_engine
    mock_engine.connect.return_value.__enter__.return_value = mock_conn
    
    # Create test data and mock to_sql on it
    df = pd.DataFrame({
        "Title": ["Item 1", "Item 2"],
        "Price_in_dollar": [10.0, 20.0],
        "Rating": [4.5, 3.0]
    })
    
    # Mock the DataFrame's to_sql method
    with patch.object(pd.DataFrame, 'to_sql') as mock_to_sql:
        # Call function
        store_to_postgre(df, "postgresql+psycopg2://postgres:inipassword@localhost:5432/fashiondb")
        
        # Assertions
        mock_create_engine.assert_called_once_with("postgresql+psycopg2://postgres:inipassword@localhost:5432/fashiondb")
        
        # Verify to_sql was called once with the correct parameters
        mock_to_sql.assert_called_once()
        mock_to_sql.assert_called_with('fashiontoscrape', con=mock_conn, if_exists='append', index=False)
    
if __name__ == "__main__":
    # This allows running the tests directly with python test_load.py
    import pytest
    pytest.main(["-v", __file__])