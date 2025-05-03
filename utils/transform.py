import pandas as pd

def transform_to_DataFrame(data):
    """Mengubah data menjadi DataFrame."""
    df = pd.DataFrame(data)
    return df

def transform_data(data, exchange_rate):
    """Menggabungkan semua transformasi data menjadi satu fungsi."""
    # Transformasi Price
    data['Price_in_dollar'] = data['Price'].replace('[$,]', '', regex=True).astype(float)
    
    data['Rating'] = data['Rating'].astype(float)
    
    # Transformasi Exchange Rate
    data['Price_in_rupiah'] = (data['Price_in_dollar'] * exchange_rate).astype(float)
    
    # Menghapus kolom redundan
    data = data.drop(columns=['Price'])
    
    # Transformasi Tipe Data
    data['Title'] = data['Title'].astype('string')
    data['Gender'] = data['Gender'].astype('string')
    data['Color'] = data['Color'].astype(int)
    data['Size'] = data['Size'].astype('string')
    
    return data