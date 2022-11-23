import uuid

from django.conf import settings
from modules.paystack import PayStackAPI as paystack_api


def generate_paystack_ref_no(transaction_id):
    return f"{settings.PAYSTACK_REF}{uuid.uuid4()}{transaction_id}".replace("-", "")


def process_payment_with_card(transaction, callback_url):
    # Generate Reference Number and update transaction

    # Generate payment link
    response = paystack_api.initialize_transaction(
        email=transaction.customer.user.email,
        amount=float(transaction.amount),
        reference=transaction.reference,
        callback_url=callback_url
    )
    if "status" in response and response["status"] is True:
        return True, response["data"]["authorization_url"]
    return False, "Error generating payment url, please try again later"


def process_payment_with_wallet():
    ...




