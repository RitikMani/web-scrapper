# Dental Stall Web Scraper

## Features
- Web scraping for dental products
- FastAPI-based web service
- Token-based authentication
- Configurable scraping settings
- Caching mechanism
- Retry strategy for failed requests

## Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `uvicorn app.main:app --reload`

## Usage
Send a POST request to `/scrape` with:
- `num_pages`: Number of pages to scrape
- `proxy`: Optional proxy URL
- Authorization header with your secret token

Example curl:
```bash
curl -X POST "http://localhost:8000/scrape?num_pages=5" \
     -H "Authorization: Bearer your_secret_token"
```

## Extensibility
- Easy to add new storage strategies
- Configurable notification methods
- Supports proxy usage