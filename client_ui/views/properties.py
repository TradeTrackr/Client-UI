from flask import Blueprint, render_template, request
import json
from client_ui.config import Config
from client_ui.utilities import authentication
from client_ui.dependencies.enquiry_api import EnquiryApi
from client_ui.dependencies.account_api import AccountApi
from client_ui.dependencies.quotes_api import QuotesAPI

properties = Blueprint('properties', __name__)

@properties.route("/properties/enquiry/<id>")
@authentication.token_required
@authentication.check_enquiry_accounts
def enquiry(id):
    enquiry = EnquiryApi().get_enquiry_and_activity(id)
    quotes = QuotesAPI().get_quotes(id)

    if enquiry != []:
        enquiry=enquiry[0]
    return render_template("pages/properties/enquiry.html",
                            error="none",
                            CDN_URL=Config.CDN_URL,
                            categories=json.loads(categories),
                            quotes=quotes,
                            enquiry=enquiry
                        )


@properties.route("/properties/enquiries")
@authentication.token_required
def enquiries():
    enquiries = EnquiryApi().get_enquiries()

    return render_template("pages/properties/enquiries.html",
                            error="none",
                            CDN_URL=Config.CDN_URL,
                            enquiries_list=enquiries
                        )


@properties.route("/user/profile/<email>")
@authentication.token_required
@authentication.check_enquiry_accounts
def user_profile(email):
    enquiry = EnquiryApi().get_user_properties_and_history(email)
    return render_template("pages/properties/user.html",
                            error="none",
                            CDN_URL=Config.CDN_URL,
                            email=email,
                            enquiry=enquiry
                        )

@properties.route("/properties/new_quote", methods=["POST"])
def new_quote():
    post_data = request.form
    new_quote = QuotesAPI().new_quote(post_data)
    EnquiryApi().update_enquiry_status('Quote Sent', post_data.get('enquiry_id'))

    return new_quote