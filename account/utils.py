import logging

from account.models import Transaction
from modules.paystack import PayStackAPI as paystack_api


def log_request(*args):
    for arg in args:
        logging.info(arg)


def perform_payment_verification(reference):
    status = "pending"
    if not Transaction.objects.filter(reference=reference).exists():
        return False, "Transaction not found"

    # Call PayStack to verify transaction
    response = paystack_api.verify_transaction(reference)
    if "status" in response:
        if response["status"] is True:
            status = response["data"]["status"]

    transaction = Transaction.objects.get(reference=reference)
    transaction.status = status
    transaction.save()

    return True, transaction

