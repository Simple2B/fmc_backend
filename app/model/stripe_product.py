from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class StripeProduct(Base):
    __tablename__ = "stripe_products"

    id = Column(Integer, primary_key=True)
    stripe_product_id = Column(String(64), nullable=False)
    price_id = Column(Integer, ForeignKey("stripe_product_prices.id"))
    name = Column(String(64), nullable=False)
    description = Column(String(64), default="")

    created = Column(Integer, nullable=False)  # timestamp from stripe

    price = relationship("StripeProductPrice", viewonly=True, uselist=False)

    def __repr__(self):
        return f"<{self.id}: {self.name}>"


class StripeProductPrice(Base):
    __tablename__ = "stripe_product_prices"

    id = Column(Integer, primary_key=True)

    stripe_price_id = Column(String(64), nullable=False)
    currency = Column(String(32), nullable=False, default="usd")
    created = Column(Integer, nullable=False)  # timestamp from stripe
    unit_amount = Column(Integer, nullable=False, default=999)  # price in cents

    def __repr__(self):
        return f"<{self.id}: {self.unit_amount}>"
