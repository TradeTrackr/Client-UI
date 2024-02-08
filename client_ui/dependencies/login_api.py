import json
import requests
from flask import current_app, g
from client_ui.config import Config

class LoginApi():

    def update_password(self, payload):
        current_app.logger.info("updating password")

        url = Config.LOGIN_API_ENDPOINT + "/update_pass"
        headers = {"Content-type": "application/json", "Accept": "text/plain"}

        response = requests.request(
            "POST", url, data=json.dumps(payload), headers=headers
        )
        return json.loads(response.text)  

    def verify_login(self, payload):
        current_app.logger.info("validating login")

        url = Config.LOGIN_API_ENDPOINT + "/trader/login"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        response = requests.request(
            "POST", url, data=payload, headers=headers
        )
        print(response.text)
        return json.loads(response.text)

    def reset_pass(self, payload):

        url = Config.LOGIN_API_ENDPOINT + "/reset_pass"
        headers = {"Content-type": "application/json", "Accept": "text/plain"}

        response = g.requests.request(
            "POST", url, data=json.dumps(payload), headers=headers
        )

        return json.loads(response.text)
