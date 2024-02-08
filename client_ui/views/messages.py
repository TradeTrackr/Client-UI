from flask import request, Blueprint, Response, jsonify, current_app, render_template
import json
from client_ui.config import Config

messages = Blueprint('messages', __name__)

@messages.route("/messages")
def check_status():
    return Response(response=json.dumps({
        "app": Config.APP_NAME,
        "status": "OK",
        "headers": request.headers.to_list()
    }),  mimetype='application/json', status=200)

