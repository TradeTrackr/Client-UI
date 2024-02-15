import json
import requests
from flask import session
from client_ui.config import Config

class AccountApi():

    def get_magic_link(self, email, url):
        params = {
            "email": email,
            "url": url
        }

        headers = {
            "Content-Type": "application/json"
        }

        resp = requests.get(
            Config.ACCOUNT_API_ENDPOINT + "/user/get_magic_link",
            data=json.dumps(params),
            headers=headers
        )

        return resp.text

    def get_trader_account_from_url(self, url):
        params = {
            "url": url
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {session['access_token']}"
        }
        resp = requests.get(
            Config.ACCOUNT_API_ENDPOINT + "/trader/check_trader_url",
            headers=headers,
            data=json.dumps(params),
        )

        return resp.text

    def get_trader_account(self, id):

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {session['access_token']}"
        }
        resp = requests.get(
            Config.ACCOUNT_API_ENDPOINT + f"/trader/get_trader/{id}",
            headers=headers
        )

        return json.loads(resp.text)


    def get_categories(self):

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {session['access_token']}"
        }
        resp = requests.get(
            Config.ACCOUNT_API_ENDPOINT + f"/category/get_categories/{session['id']}",
            headers=headers
        )

        return resp.text
