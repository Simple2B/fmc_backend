from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import stripe
from stripe.http_client import RequestsClient

import app.model as m
import app.schema as s
from tests.fixture import TestData

stripe.default_http_client = RequestsClient()  # assigning the default HTTP client


def test_get_products(
    client: TestClient,
    test_data: TestData,
    db: Session,
):
    response = client.get("api/stripe/coach/products")
    assert response
    resp_obj = s.Product.parse_obj(response.json())
    product = (
        db.query(m.StripeProduct)
        .filter_by(
            stripe_product_id=test_data.test_subscription_product.stripe_product_id
        )
        .first()
    )
    assert product
    assert resp_obj.stripe_product_id == product.stripe_product_id


def test_create_coach_sub(
    client: TestClient,
    test_data: TestData,
    db: Session,
):
    ...
