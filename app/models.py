from pydantic import BaseModel, Field
from typing import Optional

class ProductModel(BaseModel):
    product_title: str = Field(..., description="Product title")
    product_price: str = Field(..., description="Product price")
    path_to_image: Optional[str] = Field(None, description="Path to product image")