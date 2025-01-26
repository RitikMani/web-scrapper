import json
from typing import List, Dict
from cachetools import LRUCache
from app.models import ProductModel

class StorageManager:
    def __init__(self, cache_size: int = 1000):
        self.cache = LRUCache(maxsize=cache_size)
        self.json_file_path = 'products.json'

    def update_product(self, product: ProductModel) -> bool:
        """
        Update product in cache and JSON if price has changed
        """
        cache_key = product.product_title
        existing_product = self.cache.get(cache_key)

        # Only update if price is different
        if not existing_product or existing_product.product_price != product.product_price:
            self.cache[cache_key] = product
            self._save_to_json()
            return True
        return False

    def _save_to_json(self):
        """Save cached products to JSON file"""
        products = list(self.cache.values())
        with open(self.json_file_path, 'w', encoding='utf-8') as f:
            json.dump([p.dict() for p in products], f, indent=4, ensure_ascii=False)

    def get_all_products(self) -> List[ProductModel]:
        """Retrieve all products"""
        return list(self.cache.values())