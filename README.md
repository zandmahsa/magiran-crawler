# Crawler & Laravel API

This project is a crawler designed to scrape the **Magiran** website and collect information about **professors from Qom University**. The project consists of two main components:

((Crawler (Python)**: It scrapes the author pages, extracts metadata such as article titles, keywords, language, and publication information, and stores the extracted data into a json.json file. The crawler leverages requests and BeautifulSoup to fetch and parse HTML content.

**Laravel API**: The Laravel backend manages the scraped data. The models for Author and Paper define relationships and handle the CRUD operations for the database. The crawler output can be integrated into the Laravel API to store the scraped information into a database.

## Features
- Scrapes article information (title, authors, keywords, language, etc.).
- Stores the scraped data into a `json.json` file.
- Laravel models (User, Paper, Author) handle data operations.
  
## Requirements
### Python (Crawler)
- Python 3.x
- Python packages:
  - `requests`
  - `BeautifulSoup4`

### Laravel (API)
- PHP 8.x or higher
- Composer
- MySQL or SQLite

## How to Run

### Python Crawler

1. Clone the repository and navigate to the project folder.
2. Install required Python packages: `requests`, `BeautifulSoup4`
3. Modify links.txt to add the target URLs you want to scrape.
4. Run the crawler: `python crawler.py`

### Laravel API:

1. Install dependencies:
`composer install`
2. Set up your .env file for database connection.
3. Run migrations:
`php artisan migrate`
4. Run the Laravel development server:
`php artisan serve`
The API is now ready to receive data (from the crawler) via POST requests or other CRUD operations.

