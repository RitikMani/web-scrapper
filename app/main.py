from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List

from app.config import settings
from app.models import ProductModel
from app.scrapers import WebScraper
from app.storage import StorageManager
from app.notifications import NotificationHandler

app = FastAPI(title="Dental Stall Web Scraper")

security = HTTPBearer()

def validate_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Simple token authentication"""
    if credentials.credentials != settings.SECRET_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

@app.post("/scrape", response_model=List[ProductModel])
async def scrape_products(
    num_pages: int = 5, 
    proxy: str = None, 
    _: HTTPAuthorizationCredentials = Depends(validate_token)
):
    """
    Scrape product information from Dental Stall website
    
    :param num_pages: Number of pages to scrape (default 5)
    :param proxy: Optional proxy URL
    :return: List of scraped products
    """
    scraper = WebScraper(proxy)
    storage = StorageManager()
    
    total_products = 0
    updated_products = 0
    
    for page in range(1, num_pages + 1):
        products = scraper.scrape_page(page)
        total_products += len(products)
        
        for product in products:
            if storage.update_product(product):
                updated_products += 1
    
    NotificationHandler.notify(total_products, updated_products)
    
    return storage.get_all_products()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)