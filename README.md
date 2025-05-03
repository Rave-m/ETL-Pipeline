# ETL Web Scraping Project

This project implements an ETL (Extract, Transform, Load) pipeline for scraping fashion product data from websites and storing it in a PostgreSQL database.

## Directory Structure

```
├── utils/               # Core ETL functionality
│   ├── __init__.py      # Package initialization
│   ├── extract.py       # Web scraping functionality
│   ├── transform.py     # Data transformation
│   └── load.py          # Database loading
├── test/                # Test suite
│   ├── __init__.py
│   ├── test_extract.py  # Tests for extraction
│   ├── test_transform.py# Tests for transformation
│   └── test_load.py     # Tests for loading
└── main.py              # Main ETL script
```

## Setup

### Prerequisites

- Python 3.8+
- PostgreSQL database

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/ETL-scraping.git
   cd ETL-scraping
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/MacOS
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up PostgreSQL database:
   - Create a database named `fashiondb`
   - Update the database URL in main.py if needed

## Running the ETL Pipeline

Run the main script to execute the full ETL pipeline:

```bash
python main.py
```

### Configuration Options

You can modify the following parameters in main.py:

- `BASE_URL` - The fashion website URL to scrape
- `DB_URL` - Database connection string
- `EXCHANGE_RATE` - Currency exchange rate for price conversion

## Running Tests

### Run All Tests

To run the complete test suite:

```bash
pytest -v test/
```

### Run Individual Test Files

To run specific test modules:

```bash
# Test extraction functionality
python -m pytest test/test_extract.py -v

# Test transformation functionality
python -m pytest test/test_transform.py -v

# Test loading functionality
python -m pytest test/test_load.py -v
```

## ETL Components

### Extract (`utils/extract.py`)

Scrapes fashion product data from websites including:

- Product titles
- Prices
- Ratings
- Colors
- Sizes
- Gender categorization

### Transform (`utils/transform.py`)

Processes the raw data by:

- Converting prices to numeric values
- Adding currency conversion
- Standardizing data types
- Creating a clean pandas DataFrame

### Load (`utils/load.py`)

Stores the processed data in PostgreSQL:

- Creates/updates the `fashiontoscrape` table
- Handles database connection and transaction management
- Provides error handling for database operations

## Troubleshooting

If you encounter errors:

1. Make sure PostgreSQL is running and accessible
2. Check your database credentials in the connection string
3. Verify internet connectivity for web scraping
4. Run individual tests to isolate the issue

## License

This project is licensed under the MIT License - see the LICENSE file for details.
