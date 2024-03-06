from client_ui import app
from client_ui.views import general, login, dashboard, messages, enquiries, properties

def register_blueprints(app):
    """
    Adds all blueprint objects into the app.
    """
    app.register_blueprint(general.general)
    app.register_blueprint(login.login)
    app.register_blueprint(dashboard.dashboard)
    app.register_blueprint(messages.messages)
    app.register_blueprint(enquiries.enquiries)
    app.register_blueprint(properties.properties)

    # All done!
    app.logger.info("Blueprints registered")
