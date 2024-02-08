import json
import requests
from flask import session
from client_ui.config import Config

class QuotesAPI():

    def get_quotes(self, id):

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {session['access_token']}"
        }

        resp = requests.get(
            Config.QUOTES_API_ENDPOINT + f"/quote/get_quotes/{id}",
            headers=headers,
        )

        return json.loads(resp.text)

    def get_company_calendar_quotes(self):

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {session['access_token']}"
        }

        resp = requests.get(
            Config.QUOTES_API_ENDPOINT + f"/quote/get_company_quotes/{session['id']}",
            headers=headers,
        )

        return resp.text


    def new_quote(self, params):

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {session['access_token']}"
        }
        params = dict(params)
        params['status'] = 'new'
        params['company_id'] = session['id']

        if params.get('category_id'):
            params['category_id'] = int(params['category_id'])

        if not params.get('all_day'):
            params['all_day'] = False

        resp = requests.post(
            Config.QUOTES_API_ENDPOINT + "/quote/new",
            data=json.dumps(params),
            headers=headers,
        )
        return resp.text

    def new_event(self, params):

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {session['access_token']}"
        }
        params = dict(params)
        params['status'] = 'new'
        params['company_id'] = session['id']

        if not params.get('all_day'):
            params['all_day'] = False


        print(params)
        resp = requests.post(
            Config.QUOTES_API_ENDPOINT + "/event/new",
            data=json.dumps(params),
            headers=headers,
        )
        return resp.text

    def update_event(self, params, id):

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {session['access_token']}"
        }
        resp = requests.patch(
            Config.QUOTES_API_ENDPOINT + f"/event/update/{id}",
            data=json.dumps(params),
            headers=headers,
        )
        return resp.text
