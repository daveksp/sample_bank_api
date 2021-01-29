from flask import Flask

from bank_api import config
from bank_api.app_factory.configure_logging import configure_logging
from bank_api.app_factory.initialize_extensions import initialize_extensions
from bank_api.app_factory.register_blueprints import register_blueprints
from bank_api.extensions import db
from bank_api.api.utils import project_path


def create_app(package_name, package_path, settings_override=None,
               extensions=None):
    """Returns a Flask application instance configured with plants
    functionality for this application.

    :param package_name: application package name
    :param package_path: application package path
    :param settings_override: a dictionary or path to file of settings to
        override
    :param extensions: an array of instances of additional extensions to
        initialize on the app
    """
    app = Flask(package_name)
    app.config.from_object(config.Common())

    app.config.from_pyfile(project_path('settings.cfg'), silent=True)

    if settings_override:
        if isinstance(settings_override, str):
            app.config.from_pyfile(settings_override, silent=True)
        else:
            app.config.update(settings_override)

    register_blueprints(app, package_name, package_path)
    common_extensions = frozenset([db])
    initialize_extensions(app, common_extensions)

    initialize_extensions(app, extensions)
    configure_logging(app)

    return app
