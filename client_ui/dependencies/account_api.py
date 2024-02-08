import json
import requests
from flask import session
from client_ui.config import Config

class TraderAccountApi():

    def get_account(self):
        params = {"id": id}

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {session['access_token']}"
        }

        resp = requests.get(
            Config.ACCOUNT_API_ENDPOINT + "/trader/get_company_by_email",
            data=json.dumps(params),
            headers=headers
        )

        return json.loads(resp.text)

    def get_categories(self):

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {session['access_token']}"
        }
        print(headers)
        print(Config.ACCOUNT_API_ENDPOINT + f"/category/get_categories/{session['id']}")
        resp = requests.get(
            Config.ACCOUNT_API_ENDPOINT + f"/category/get_categories/{session['id']}",
            headers=headers
        )

        return resp.text
