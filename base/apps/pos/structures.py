from pydantic import BaseModel
from typing import List


class OrderStructure(BaseModel):
    total: float
    payment_method: int
    author: int


class ProductOrderStructure(BaseModel):
    product: int
    quantity: float
    # price: float


class SellStructure(BaseModel):
    order: OrderStructure
    product_orders: List[ProductOrderStructure]
