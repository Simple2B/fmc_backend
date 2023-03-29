from functools import lru_cache

import stripe
from fastapi import Depends

from app.config import get_settings, Settings


@lru_cache
def get_stripe(settings: Settings = Depends(get_settings)):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    return stripe
