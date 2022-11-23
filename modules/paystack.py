import json

import requests
from django.conf import settings

base_url = settings.PAYSTACK_BASE_URL
secret = settings.PAYSTACK_SECRET_KEY
ref = settings.PAYSTACK_REF


class PayStackAPI:
    @classmethod
    def get_header(cls):
        data = dict()
        data["Content-Type"] = "application/json"
        data["Authorization"] = f"Bearer {secret}"
        return data

    @classmethod
    def initialize_transaction(cls, **kwargs):
        from account.utils import log_request
        url = f"{base_url}/transaction/initialize"
        header = cls.get_header()

        amount = kwargs.get("amount") * 100

        data = dict()
        data["email"] = kwargs.get("email")
        data["reference"] = kwargs.get("reference")
        data["callback_url"] = kwargs.get("callback_url")
        data["amount"] = amount
        data["currency"] = "NGN"

        payload = json.dumps(data)
        response = requests.request("POST", url, data=payload, headers=header).json()
        log_request(f"url: {url}, payload: {payload}, response: {response}")
        return response

    @classmethod
    def verify_transaction(cls, reference):
        from account.utils import log_request
        url = f"{base_url}/transaction/verify/{reference}"
        header = cls.get_header()
        response = requests.request("GET", url, headers=header).json()
        log_request(f"url: {url}, response: {response}")
        return response






