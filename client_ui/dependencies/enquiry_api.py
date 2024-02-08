import json
import requests
from flask import current_app, g, request, session
from client_ui.config import Config

class EnquiryApi():

    def get_enquiries(self):

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {session['access_token']}"
        }

        resp = requests.get(
            Config.ENQUIRY_API_ENDPOINT + f"/get_enquirys/{session['id']}",
            headers=headers,
        )

        return json.loads(resp.text)

    def get_new_enquiries(self):

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {session['access_token']}"
        }

        resp = requests.get(
            Config.ENQUIRY_API_ENDPOINT + f"/get_new_enquirys/{session['id']}",
            headers=headers,
        )

        return json.loads(resp.text)

    def get_enquiry_to_check(self, params):

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {session['access_token']}"
        }

        resp = requests.get(
            Config.ENQUIRY_API_ENDPOINT + f"/get_enquiry_to_check",
            headers=headers,
            data=json.dumps(params)
        )

        return json.loads(resp.text)

    def get_enquiry(self, id):

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {session['access_token']}"
        }

        resp = requests.get(
            Config.ENQUIRY_API_ENDPOINT + f"/get_enquiry/{id}/{session['id']}",
            headers=headers,
        )

        return json.loads(resp.text)

    def update_enquiry_status(self, status, id):

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {session['access_token']}"
        }
        params = {
            'status': status
        }

        resp = requests.put(
            Config.ENQUIRY_API_ENDPOINT + "/enquiry/{id}",
            data=json.dumps(params),
            headers=headers,
        )
        return resp.text

    def get_enquiry_and_activity(self, id):

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {session['access_token']}"
        }

        resp = requests.get(
            Config.ENQUIRY_API_ENDPOINT + f"/get_enquiry/{id}/{session['id']}",
            headers=headers,
        )

        return json.loads(resp.text)

    def get_user_properties_and_history(self, email):

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {session['access_token']}"
        }
        data = {
            "email": email
        }
        resp = requests.get(
            Config.ENQUIRY_API_ENDPOINT + f"/get_user_enquiries/{session['id']}",
            headers=headers,
            data=json.dumps(data)
        )

        return json.loads(resp.text)