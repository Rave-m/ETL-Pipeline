from utils import scrape_fashion, transform_data, store_to_postgre, transform_to_DataFrame, store_to_csv
import csv

def main():
    """Fungsi utama untuk keseluruhan proses scraping, transformasi data, dan penyimpanan."""
    BASE_URL = 'https://fashion-studio.dicoding.dev'
    
    # Menjalankan scraping untuk mengambil data buku
    all_fashions_data = scrape_fashion(BASE_URL)
    
    # Jika data berhasil diambil, lakukan transformasi dan simpan ke PostgreSQL
    if all_fashions_data:
        try:
            
            
            # Mengubah data menjadi DataFrame
            DataFrame = transform_to_DataFrame(all_fashions_data)
            
            # Mentransformasikan data (misalnya konversi mata uang, rating, dll)
            DataFrame = transform_data(DataFrame, 16000)  # Anggap 20000 adalah nilai tukar yang diperlukan

            print("DataFrame:\n", DataFrame.head())  # Menampilkan 5 data teratas untuk verifikasi
            
            # Menyimpan data ke CSV
            store_to_csv(DataFrame, 'fashion_data.csv')  # Menyimpan data ke file CSV
            
            # Menyimpan data ke PostgreSQL
            DATABASE_URL = 'postgresql+psycopg2://postgres:inipassword@localhost:5432/fashiondb'
            store_to_postgre(DataFrame, DATABASE_URL)  # Memanggil fungsi untuk menyimpan ke database

        except Exception as e:
            print(f"Terjadi kesalahan dalam proses: {e}")
    else:
        print("Tidak ada data yang ditemukan.")

if __name__ == '__main__':
    main()