from flask import Blueprint, render_template, request
import json
from client_ui.config import Config
from client_ui.utilities import authentication
from client_ui.dependencies.enquiry_api import EnquiryApi
from client_ui.dependencies.account_api import AccountApi
from client_ui.dependencies.quotes_api import QuotesAPI

properties = Blueprint('properties', __name__)

@properties.route("/properties")
@authentication.token_required
def get_properties():
    enquiries = EnquiryApi().get_enquiries()

    return render_template("pages/properties/properties.html",
                            error="none",
                            CDN_URL=Config.CDN_URL,
                            properties_list=organise_enquiries_by_address(enquiries)
                        )


def organise_enquiries_by_address(enquiries_list):
    new_enq_dict = {}

    for enquiry in enquiries_list:
        address_string = f'{enquiry.get("address_line1", "")} {enquiry.get("address_line2", "")} {enquiry.get("postcode", "")}'.replace(' ', '_')

        if not new_enq_dict.get(address_string):
            new_enq_dict[address_string] = {}

        new_enq_dict[address_string]['address_line1'] =  f'{enquiry.get("address_line1", "")} {enquiry.get("address_line2", "")}'
        new_enq_dict[address_string]['address_postcode'] =  f'{enquiry.get("postcode", "")}'

    return new_enq_dict
