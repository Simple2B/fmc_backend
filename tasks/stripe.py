from invoke import task

from app.logger import log
from app.dependency.controller import get_stripe
from app.config import Settings, get_settings
import app.model as m
from app.database import get_db, Session


settings: Settings = get_settings()
stripe = get_stripe(settings)
db: Session = get_db().__next__()


@task
def get_coach_subscription(_):
    product = (
        db.query(m.StripeProduct)
        .filter_by(stripe_product_id=settings.COACH_SUBSCRIPTION_PRODUCT_ID)
        .first()
    )
    if not product:
        stripe_product = stripe.Product.retrieve(settings.COACH_SUBSCRIPTION_PRODUCT_ID)
        stripe_price = stripe.Price.retrieve(stripe_product.default_price)
        # creating price
        price = m.StripeProductPrice(
            stripe_price_id=stripe_price.id,
            currency=stripe_price.currency,
            created=stripe_price.created,
            unit_amount=stripe_price.unit_amount,
        )
        db.add(price)
        db.flush()
        db.refresh(price)

        product = m.StripeProduct(
            stripe_product_id=stripe_product.id,
            price_id=price.id,
            name=stripe_product.name,
            description=stripe_product.description,
            created=stripe_product.created,  # timestamp from stripe
        )
        db.add(product)
        db.commit()
    print()
    log(log.INFO, "Product and price created successfully")
