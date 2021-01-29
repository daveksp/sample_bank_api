from bank_api.app_factory import create_app as factory_create_app

from bank_api.api.extensions import schemas
from bank_api.api.logging import setup_logging
from .handlers import setup_handlers


def create_app(settings_override=None):
    """Returns an api application instance"""
    extensions = frozenset([schemas])

    app = factory_create_app(__name__, __path__, settings_override, extensions)

    if not app.extensions:
        app.extensions = {}

    # setup logging before handlers for all the effects of the handlers
    # to be present in the logs
    setup_logging(app)
    setup_handlers(app)

    # causing server errors in prod. disabled for now
    # newrelic.agent.initialize('newrelic.ini')

    return app
