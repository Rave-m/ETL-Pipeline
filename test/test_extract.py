import sys
import os
import time
import requests
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup

# Add the project root to the path so we can import the utils package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.extract import fetching_content, extract_fashion_data, scrape_fashion

# ====================== EXTRACT TESTS ======================

@patch('utils.extract.requests.Session')
def test_fetching_content_success(mock_session):
    """Test successful content fetching"""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.content = b'<html><body>Test Content</body></html>'
    mock_session.return_value.get.return_value = mock_response
    
    # Call the function
    content = fetching_content("https://example.com")
    
    # Assertions
    assert content == b'<html><body>Test Content</body></html>'
    mock_session.return_value.get.assert_called_once()

@patch('utils.extract.requests.Session')
def test_fetching_content_failure(mock_session):
    """Test failure case for content fetching"""
    # Setup mock to raise exception
    mock_session.return_value.get.side_effect = requests.exceptions.RequestException("HTTP Error")
    
    # Call the function
    content = fetching_content("https://example.com")
    
    # Assertions
    assert content is None

def test_extract_fashion_data():
    """Test extracting fashion data from HTML"""
    # Create a mock product HTML element
    html = '''
    <div class="collection-card">
        <h3 class="product-title">Test Fashion Item</h3>
        <div class="price-container">
            <span class="price">$99.99</span>
        </div>
        <div class="product-details">
            <p>Rating: ⭐ 4.5 / 5</p>
            <p>5 Colors</p>
            <p>Size: L</p>
            <p>Gender: Women</p>
        </div>
    </div>
    '''
    soup = BeautifulSoup(html, 'html.parser')
    product = soup.find('div', class_='collection-card')
    
    # Extract fashion data
    fashion = extract_fashion_data(product)
    
    # Assertions
    assert fashion['Title'] == 'Test Fashion Item'
    assert fashion['Price'] == '$99.99'
    assert fashion['Rating'] == '4.5'
    assert fashion['Color'] == '5'
    assert fashion['Size'] == 'L'
    assert fashion['Gender'] == 'Women'

@patch('utils.extract.fetching_content')
@patch('utils.extract.extract_fashion_data')
@patch('utils.extract.time.sleep')  # Mock sleep to speed up tests
def test_scrape_fashion(mock_sleep, mock_extract_data, mock_fetch):
    """Test scraping fashion data from multiple pages"""
    # Mock responses for two pages
    page1_html = '''
    <html>
        <body>
            <div class="collection-card"></div>
            <div class="collection-card"></div>
            <li class="next">Next</li>
        </body>
    </html>
    '''
    
    page2_html = '''
    <html>
        <body>
            <div class="collection-card"></div>
            <li class="next disabled">Next</li>
        </body>
    </html>
    '''
    
    # Configure mock to return different content for different URLs
    mock_fetch.side_effect = [
        page1_html,  # First page
        page2_html   # Second page
    ]
      # Configure mock extract data to return dummy product data
    mock_extract_data.side_effect = [
        {
            "Title": "Mock Product 1",
            "Price": "$10.00",
            "Rating": "4.5",
            "Color": "3",
            "Size": "S",
            "Gender": "Men"
        },
        {
            "Title": "Mock Product 2",
            "Price": "$20.00",
            "Rating": "4.0",
            "Color": "2",
            "Size": "M",
            "Gender": "Women"
        },
        {
            "Title": "Mock Product 3",
            "Price": "$30.00",
            "Rating": "3.5",
            "Color": "4",
            "Size": "L",
            "Gender": "Men"
        }
    ]
    
    # Call the function
    data = scrape_fashion("https://example.com")
    
    # Assertions
    print(f"Data length in test: {len(data)}")
    assert len(data) == 3  # 2 products from page 1 + 1 from page 2
    assert mock_fetch.call_count == 2
    assert mock_extract_data.call_count == 3

if __name__ == "__main__":
    # This allows running the tests directly with python test_extract.py
    import pytest
    pytest.main(["-v", __file__])