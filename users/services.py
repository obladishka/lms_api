import stripe

from config.settings import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY


def create_price(amount: float) -> stripe.Price:
    """Creating price to perform payment."""

    return stripe.Price.create(currency="rub", unit_amount=amount * 100, product_data={"name": "LMS Payment"})


def get_payment_link(price: stripe.Price) -> tuple[str, str]:
    """Creating session and getting link for payment."""

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/users/login",
        line_items=[{"price": price.id, "quantity": 1}],
        mode="payment",
    )
    return session.get("url")
