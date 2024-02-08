from flask import Flask, g, request
import uuid
import requests

app = Flask(__name__)

app.config.from_pyfile("config.py")


@app.before_request
def before_request():
    # Sets the transaction trace id into the global object if it has been provided in the HTTP header from the caller.
    # Generate a new one if it has not. We will use this in log messages.
    g.trace_id = request.headers.get('X-Trace-ID', uuid.uuid4().hex)
    # We also create a session-level requests object for the app to use with the header pre-set, so other APIs will
    # receive it. These lines can be removed if the app will not make requests to other LR APIs!
    g.requests = requests.Session()
    g.requests.headers.update({'X-Trace-ID': g.trace_id})


#these imports must be included after the app object has been created as it is imported in them
from client_ui.blueprints import register_blueprints
from client_ui.extensions import register_extensions

# Register any extensions we use into the app
register_extensions(app)
register_blueprints(app)
