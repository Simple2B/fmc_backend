from pydantic import BaseModel, HttpUrl


class Price(BaseModel):
    stripe_price_id: str
    currency: str
    created: int
    unit_amount: int

    class Config:
        orm_mode = True


class Product(BaseModel):
    stripe_product_id: str
    name: str
    description: str
    created: int
    price: Price

    class Config:
        orm_mode = True


class CheckoutSession(BaseModel):
    url: HttpUrl
