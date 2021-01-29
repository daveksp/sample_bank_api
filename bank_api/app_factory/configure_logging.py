import logging.handlers


def configure_logging(app, context='api'):
    """configure logging for specific app"""
    app.logger.setLevel(logging.DEBUG)
    level = app.config['LOG_LEVEL']

    file_handler = logging.handlers.TimedRotatingFileHandler(
        app.config['LOG_FILE'], when='midnight', backupCount=1)

    file_handler.setLevel(level)
    app.logger.addHandler(file_handler)
