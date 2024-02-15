from flask import (
    redirect,
    Blueprint,
    render_template,
    request,
    current_app,
    session,
    jsonify,
    g,
)
import requests
import json
from client_ui.config import Config
from client_ui.dependencies.account_api import AccountApi
from client_ui.dependencies.sqs import EmailSqsSender
from client_ui.dependencies.enquiry_api import EnquiryApi

login = Blueprint("login", __name__)

# Routes definition
@login.route("/login")
def login_page():
    return LoginManager.display_login_page()

@login.route("/login/validate_login", methods=["POST"])
def login_validate():
    return LoginManager.validate_login()


class LoginManager:

    @staticmethod
    def display_login_page():
        session["next"] = request.args.get("next", "/")
        if session.get("keep_me_logged_in_company") == "logged_in":
            return redirect("./home")
        return render_template("pages/login/display_logins.html", error="none", CDN_URL=Config.CDN_URL)

    @staticmethod
    def validate_login():
        post_data = request.form

        payload = {}
        payload["email"] = post_data.get("email").lower()

        full_base_url = request.url_root.strip('/')

        get_company_details = AccountApi().get_trader_account_from_url(full_base_url)
        if get_company_details is False:
            return jsonify({"result":"error-wrong-url"})

        get_company_details = json.loads(get_company_details)
        json_Enqs = EnquiryApi().check_any_enuqiries(post_data.get("email").lower(), get_company_details['id'])
        if json_Enqs == []:
            return jsonify({"result":"error-password-username"})

        json_data = AccountApi().get_magic_link(post_data.get("email").lower(), get_company_details['company_url'])
        if "detail" in json_data:        
            if json_data["detail"] == "Incorrect email or password":
                return jsonify({"result":"error-password-username"})

        json_data=json.loads(json_data)
        if 'magic_link' in json_data:

            EmailSqsSender().send_message({
                "type": "Magic Link",
                "email": post_data.get("email").lower(),
                "from_email": get_company_details['company_response_email'],
                "name": json_Enqs[0]["full_name"],
                "title": f"Your magic link has arrived!",
                'trader_details': get_company_details,
                'template': 'magic_link',
                'magic_link': json_data["magic_link"]
            })
        

            return jsonify({"result": "OK"})

        return jsonify({"result":"internal-error"})
