from pydantic import BaseModel
from typing import List


class OrderStructure(BaseModel):
    total: float
    payment_method: int


class ProductOrderStructure(BaseModel):
    product: int
    quantity: float
    price: float


class SellStructure(BaseModel):
    order: OrderStructure
    product_orders: List[ProductOrderStructure]


class detailCashControlStructure(BaseModel):
    key: int
    payment_method: str
    sales: int
    total: float


class cashControlStructure(BaseModel):
    total: float
    sales: int
    detail: List[detailCashControlStructure]
