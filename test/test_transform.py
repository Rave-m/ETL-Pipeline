
import sys
import os
import pandas as pd

# Add the project root to the path so we can import the utils package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.transform import transform_to_DataFrame, transform_data

def test_transform_to_DataFrame():
    """Test converting data to DataFrame"""
    # Input data
    data = [
        {"Title": "Item 1", "Price": "$10.00", "Rating": "4.5"},
        {"Title": "Item 2", "Price": "$20.00", "Rating": "3.0"}
    ]
    
    # Transform to DataFrame
    df = transform_to_DataFrame(data)
    
    # Assertions
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 3)
    assert list(df.columns) == ["Title", "Price", "Rating"]

def test_transform_data():
    """Test data transformation"""
    # Create test DataFrame
    data = pd.DataFrame({
        "Title": ["Item 1", "Item 2"],
        "Price": ["$10.00", "$20.00"],
        "Rating": ["4.5", "3.0"],
        "Gender": ["Men", "Women"],
        "Color": ["3", "5"],
        "Size": ["M", "L"]
    })
    
    # Transform data
    exchange_rate = 15000
    result = transform_data(data, exchange_rate)
    
    # Assertions
    assert "Price_in_dollar" in result.columns
    assert "Price_in_rupiah" in result.columns
    assert "Price" not in result.columns  # Check that original Price was dropped
    assert result["Price_in_dollar"][0] == 10.0
    assert result["Price_in_rupiah"][0] == 150000.0
    assert result["Rating"][0] == 4.5
    assert result["Color"].dtype == "int64"
    
if __name__ == "__main__":
    # This allows running the tests directly with python test_load.py
    import pytest
    pytest.main(["-v", __file__])