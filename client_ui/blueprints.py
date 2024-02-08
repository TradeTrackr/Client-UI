from client_ui import app
from client_ui.views import general, login, dashboard, messages

def register_blueprints(app):
    """
    Adds all blueprint objects into the app.
    """
    app.register_blueprint(general.general)
    app.register_blueprint(login.login)
    app.register_blueprint(dashboard.dashboard)
    app.register_blueprint(messages.messages)

    # All done!
    app.logger.info("Blueprints registered")
