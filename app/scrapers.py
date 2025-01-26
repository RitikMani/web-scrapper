import os
import time
import requests
from bs4 import BeautifulSoup
from typing import List, Optional

from app.models import ProductModel
from app.config import settings

class WebScraper:
    def __init__(self, proxy: Optional[str] = None):
        self.base_url = 'https://dentalstall.com/shop/page/{}/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
        }
        self.proxy = {'http': proxy, 'https': proxy} if proxy else None
        
        # Ensure images directory exists
        if not os.path.exists('images'):
            os.makedirs('images')

    def scrape_page(self, page_number: int) -> List[ProductModel]:
        """
        Scrape a single page with retry mechanism
        """
        for attempt in range(settings.MAX_RETRY_ATTEMPTS):
            try:
                url = self.base_url.format(page_number)
                response = requests.get(
                    url, 
                    headers=self.headers, 
                    proxies=self.proxy, 
                    timeout=10
                )
                response.raise_for_status()
                
                return self._parse_products(response.content)
            
            except requests.exceptions.RequestException as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < settings.MAX_RETRY_ATTEMPTS - 1:
                    time.sleep(settings.RETRY_DELAY)
                else:
                    print(f"Failed to scrape page {page_number} after {settings.MAX_RETRY_ATTEMPTS} attempts")
                    return []

    def _parse_products(self, content) -> List[ProductModel]:
        """
        Parse HTML content and extract product information
        """
        soup = BeautifulSoup(content, 'lxml')
        product_list = soup.find_all('li', class_='product')
        
        products = []
        for product in product_list:
            try:
                name = self._extract_name(product)
                price = self._extract_price(product)
                image_path = self._download_image(product)
                
                products.append(ProductModel(
                    product_title=name,
                    product_price=price,
                    path_to_image=image_path
                ))
            except Exception as e:
                print(f"Error parsing product: {e}")
        
        return products

    def _extract_name(self, product_element) -> str:
        name_element = product_element.find('h2', class_='woo-loop-product__title')
        return name_element.get_text(separator=' ', strip=True).replace('...', '').strip() if name_element else 'Unknown'

    def _extract_price(self, product_element) -> str:
        price_element = product_element.find('span', class_='woocommerce-Price-amount')
        return price_element.get_text(separator=' ', strip=True).replace('\u20b9', '').strip() if price_element else 'Price not available'

    def _download_image(self, product_element) -> Optional[str]:
        thumbnail_div = product_element.find('div', class_='mf-product-thumbnail')
        if not thumbnail_div:
            return None

        img_element = thumbnail_div.find('img')
        if not img_element:
            return None

        img_url = img_element.get('data-lazy-src') or img_element.get('src')
        if not img_url or not img_url.startswith('https://'):
            return None

        try:
            img_name = img_url.split('/')[-1]
            img_path = os.path.join('images', img_name)

            img_response = requests.get(img_url, stream=True)
            if img_response.status_code == 200:
                with open(img_path, 'wb') as f:
                    for chunk in img_response.iter_content(1024):
                        f.write(chunk)
                return img_path
        except Exception as e:
            print(f"Image download failed: {e}")

        return None