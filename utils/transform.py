import pandas as pd
import datetime

def transform_to_DataFrame(data):
    """Mengubah data menjadi DataFrame."""
    df = pd.DataFrame(data)
    return df

def check_dirty_data(data):
    """Memeriksa data kotor seperti null values, duplicates, atau anomali lainnya."""
    print("\n" + "="*50)
    print("PEMERIKSAAN DATA KOTOR")
    print("="*50)
    
    # Informasi dasar tentang data
    print(f"\nJumlah baris dan kolom: {data.shape}")
    
    # Cek nilai null/missing
    print("\nJumlah nilai yang hilang per kolom:")
    print(data.isnull().sum())
    
    # Cek data duplikat
    duplicates = data.duplicated().sum()
    print(f"\nJumlah data duplikat: {duplicates}")
    
    # Cek tipe data
    print("\nTipe data per kolom:")
    print(data.dtypes)
    
    # Statistik dasar
    print("\nStatistik dasar:")
    print(data.describe(include='all').T)
    
    # Cek nilai unik untuk kolom kategorikal
    print("\nNilai unik untuk beberapa kolom:")
    categorical_cols = data.select_dtypes(include=['object', 'string']).columns
    for col in categorical_cols:
        if len(data[col].unique()) < 20:  # Hanya tampilkan jika nilai unik tidak terlalu banyak
            print(f"\n{col}: {data[col].unique()}")
    
    print("\n" + "="*50)
    return data

def transform_data(data, exchange_rate):
    """Menggabungkan semua transformasi data menjadi satu fungsi."""
    # Memeriksa data kotor terlebih dahulu
    check_dirty_data(data)
    
    # Membuat copy eksplisit dari DataFrame untuk menghindari SettingWithCopyWarning
    data = data.copy()
    
    # Transformasi Price: Membersihkan simbol $ dan koma, lalu mengubah ke numerik
    data.loc[:, 'Price'] = data['Price'].replace('[$,]', '', regex=True).astype(float)
    # Mengkonversi Rating ke tipe float
    data.loc[:, 'Rating'] = data['Rating'].astype(float)
    
    # Membuang data dengan Rating 0.0
    rows_before = len(data)
    data = data[data['Rating'] != 0.0]
    rows_after = len(data)
    if rows_before > rows_after:
        print(f"\n{'-'*20}")
        print(f"Membuang {rows_before - rows_after} baris dengan Rating 0.0")
        print(f"{'-'*20}\n")
    
    # Mengkonversi Price dari USD ke IDR (Rupiah) dengan exchange rate
    data.loc[:, 'Price'] = (data['Price'] * exchange_rate).astype(float)
    
    # Menampilkan informasi data duplikat
    print(f"\n {'-'*20}")
    print(f"jumlah data duplicated: {data.duplicated().sum()}")
    data = data.drop_duplicates()
    print(f"jumlah data duplicated: {data.duplicated().sum()}")
    print(f"{'-'*20} \n")    # Transformasi Tipe Data
    data.loc[:, 'Title'] = data['Title'].astype('string')
    data.loc[:, 'Gender'] = data['Gender'].astype('string')
    
    # Konversi Color dari string ke integer dengan lebih ketat dan pastikan tipe data adalah numerik
    data['Color'] = pd.to_numeric(data['Color'], errors='coerce').fillna(0).astype(int)

    data.loc[:, 'Size'] = data['Size'].astype('string')
    
    # Menambahkan kolom timestamp kapan data diambil dengan format YYYY-MM-DD HH:MM:SS
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data.loc[:, 'Timestamp'] = current_time
    
    return data