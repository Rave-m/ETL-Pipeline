from utils import scrape_fashion, transform_data, store_to_postgre, transform_to_DataFrame, store_to_csv
from utils.transform import check_dirty_data
import csv
import argparse

def main(check_only=False):
    """Fungsi utama untuk keseluruhan proses scraping, transformasi data, dan penyimpanan."""
    BASE_URL = 'https://fashion-studio.dicoding.dev'
    
    # Menjalankan scraping untuk mengambil data buku
    all_fashions_data = scrape_fashion(BASE_URL)
    
    # Jika data berhasil diambil, lakukan transformasi dan simpan ke PostgreSQL
    if all_fashions_data:
        try:
            # Mengubah data menjadi DataFrame
            DataFrame = transform_to_DataFrame(all_fashions_data)
            
            # Hanya memeriksa data kotor jika flag check_only aktif
            if check_only:
                print("\nMEMERIKSA DATA KOTOR (TANPA TRANSFORMASI)")
                check_dirty_data(DataFrame)
                return
            
            # Mentransformasikan data (misalnya konversi mata uang, rating, dll)
            DataFrame = transform_data(DataFrame, 16000)  # Anggap 16000 adalah nilai tukar yang diperlukan

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
    parser = argparse.ArgumentParser(description='ETL Pipeline untuk data fashion')
    parser.add_argument('--check-only', action='store_true', 
                        help='Hanya memeriksa data kotor tanpa melakukan transformasi dan penyimpanan')
    args = parser.parse_args()
    
    main(check_only=args.check_only)