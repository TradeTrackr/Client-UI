from flask import Blueprint, render_template, request
import json
from client_ui.config import Config
from client_ui.utilities import authentication
from client_ui.dependencies.enquiry_api import EnquiryApi
from client_ui.dependencies.quotes_api import QuotesAPI
from client_ui.dependencies.account_api import AccountApi

dashboard = Blueprint('dashboard', __name__)

@dashboard.route("/home")
@authentication.token_required
def home():
    get_enquiries = EnquiryApi().get_enquiries()
    get_enquiries_address = organise_enquiries_by_address(get_enquiries)
    enquiry_ids = []
    for enquiry in get_enquiries:
        enquiry_ids.append(enquiry['id'])

    quotes = QuotesAPI().get_quotes(enquiry_ids)

    return render_template("pages/dashboard/dashboard.html",
                            error="none",
                            enquiry=get_enquiries_address,
                            quotes=quotes,
                            CDN_URL=Config.CDN_URL
                        )

@dashboard.route("/dashboard/get_quotes")
@authentication.token_required
def get_quotes():
    calendar_quotes = QuotesAPI().get_company_calendar_quotes()
    return calendar_quotes


@dashboard.route("/dashboard/new_event", methods=["POST"])
def new_event():
    post_data = request.form
    return QuotesAPI().new_event(post_data)


@dashboard.route("/dashboard/update_event/<id>", methods=["POST"])
def update_event(id):
    post_data = request.get_json()
    return QuotesAPI().update_event(post_data, id)


@dashboard.route("/dashboard/get_categories")
@authentication.token_required
def get_categories():
    return AccountApi().get_categories()


def organise_enquiries_by_address(enquiries_list):
    new_enq_dict = {}

    for enquiry in enquiries_list:
        address_string = f'{enquiry.get("address_line1", "")} {enquiry.get("address_line2", "")} {enquiry.get("postcode", "")}'.replace(' ', '_')

        if not new_enq_dict.get(address_string):
            new_enq_dict[address_string] = {}

        new_enq_dict[address_string]['address_line1'] =  f'{enquiry.get("address_line1", "")} {enquiry.get("address_line2", "")}'
        new_enq_dict[address_string]['address_postcode'] =  f'{enquiry.get("postcode", "")}'

    return new_enq_dict
