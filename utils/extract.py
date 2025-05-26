import time
import requests

from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

def fetching_content(url):
    """Mengambil konten HTML dari URL yang diberikan."""
    session = requests.Session()
    
    try:
        response = session.get(url, headers=HEADERS)
        response.raise_for_status()  # Raise an exception for 4xx/5xx responses
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Terjadi kesalahan ketika melakukan requests terhadap {url}: {e}")
        return None

def extract_fashion_data(product):
    """Mengambil data fashion berupa Title, Price, Rating, Colors, Size, Gender dari fashion studio (element html)."""

    fashion_title = product.find('h3', class_='product-title').text
    
    price_element = product.find('div', class_='price-container')
    if price_element is None:
        price = "$0.00"
    else:
        price = price_element.find('span', class_='price').text

    product_detais = product.find('div', class_='product-details')
    rating, color, size, gender = '', '', '', ''
    
    for details in product_detais.find_all('p'):
        text = details.text.strip()
        
        # Extract rating - get only the rating part after "Rating:"
        if text.startswith("Rating:"):
            # Fix for the rating extraction to handle "Rating: 4.5 / 5" format
            rating_text = text.replace("Rating:", "").strip()
            if rating_text == "Not Rated":
                rating = '0.0'
            elif "Invalid" in rating_text:
                rating = '0.0'
            else:
                # Extract the number before the slash
                rating = text.split()[2]
            
        # Extract color - get the number from "5 Colors" format
        elif "Color" in text or "Colors" in text:
            # Extract digits from the text - handles both "5 Colors" and "Color: 5"
            color = ''.join(filter(str.isdigit, text))
            
        # Extract size - get only the size value
        elif text.startswith("Size:"):
            size = text.replace("Size:", "").strip()
            
        # Extract gender - get only the gender value
        elif text.startswith("Gender:"):
            gender = text.replace("Gender:", "").strip()

    fashion = {
        "Title": fashion_title,
        "Price": price,
        "Rating": rating,
        "Color": color,
        "Size": size,
        "Gender": gender
    }

    return fashion


def scrape_fashion(base_url, delay=2):
    """Fungsi utama untuk mengambil keseluruhan data, mulai dari requests hingga menyimpannya dalam variabel data."""
    data = []
    page_number = 1
    has_next_page = True
    
    while has_next_page:
        # Generate URL based on page number
        if page_number == 1:
            url = base_url  # First page is just the base URL
        else:
            url = f"{base_url}/page{page_number}"  # Subsequent pages include page number
            
        print(f"Scraping halaman: {url}")

        content = fetching_content(url)
        if not content:
            print("Failed to fetch content. Stopping.")
            break
            
        soup = BeautifulSoup(content, "html.parser")
        product_elements = soup.find_all('div', class_='collection-card')
        
        # Check if we found any products
        if not product_elements:
            print("No products found on this page. Stopping.")
            break
        
        # Extract product data
        for product in product_elements:
            fashion = extract_fashion_data(product)
            data.append(fashion)
        # Check for next page outside the product loop
        next_button_elem = soup.find('li', class_='next')
        if next_button_elem and 'disabled' not in next_button_elem.get('class', []):
            # Next button exists and is not disabled
            page_number += 1 
            url = f"{base_url}?page={page_number}"
            print(f"Found next page. Moving to page {page_number}")
            time.sleep(delay)  # Delay before fetching next page
        else:
            print("No more pages. Scraping complete.")
            has_next_page = False

    print(f"Total products scraped: {len(data)}")
    return data