from flask import Blueprint, render_template, request, redirect
import json
from client_ui.config import Config
from client_ui.utilities import authentication
from client_ui.dependencies.enquiry_api import EnquiryApi
from client_ui.dependencies.account_api import AccountApi
from client_ui.dependencies.quotes_api import QuotesAPI

enquiries = Blueprint('enquiries', __name__)

@enquiries.route("/enquiries/enquiry/<id>")
@authentication.token_required
@authentication.check_enquiry_accounts
def get_enquiry(id):
    enquiry = EnquiryApi().get_enquiry_and_activity(id)
    quotes = QuotesAPI().get_quotes(id)

    if enquiry != []:
        enquiry=enquiry[0]
    return render_template("pages/enquiries/enquiry.html",
                            error="none",
                            CDN_URL=Config.CDN_URL,
                            quotes=quotes,
                            enquiry=enquiry
                        )

@enquiries.route("/enquiries")
@authentication.token_required
def get_enquiries():
    enquirieslist = EnquiryApi().get_enquiries()
    return render_template("pages/enquiries/enquiries.html",
                            error="none",
                            CDN_URL=Config.CDN_URL,
                            enquiries_list=enquirieslist
                        )

@enquiries.route("/enquiries/<address>")
@authentication.token_required
def get_enquiries_by_address(address):
    enquirieslist = EnquiryApi().get_enquiries()
    address_enquiries = organise_enquiries_return_address(enquirieslist, address)

    if address_enquiries == []:
        return redirect("./no-access")

    return render_template("pages/enquiries/enquiries.html",
                            error="none",
                            address=address.replace('_', ' '),
                            CDN_URL=Config.CDN_URL,
                            enquiries_list=address_enquiries
                        )


@enquiries.route("/user/profile/<email>")
@authentication.token_required
@authentication.check_enquiry_accounts
def user_profile(email):
    enquiry = EnquiryApi().get_user_properties_and_history(email)
    return render_template("pages/enquiries/user.html",
                            error="none",
                            CDN_URL=Config.CDN_URL,
                            email=email,
                            enquiry=enquiry
                        )

@enquiries.route("/enquiries/new_quote", methods=["POST"])
def new_quote():
    post_data = request.form
    new_quote = QuotesAPI().new_quote(post_data)
    EnquiryApi().update_enquiry_status('Quote Sent', post_data.get('enquiry_id'))

    return new_quote

def organise_enquiries_return_address(enquiries_list, address):
    enq_list = []

    for enquiry in enquiries_list:
        address_string = f'{enquiry.get("address_line1", "")} {enquiry.get("address_line2", "")} {enquiry.get("postcode", "")}'.replace(' ', '_')

        if address == address_string:
            enq_list.append(enquiry)

    return enq_list
