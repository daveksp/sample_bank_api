import logging


class Common(object):

    DEBUG = True

    LOG_FILE = "/tmp/bank_api.log"
    LOG_LEVEL = logging.DEBUG

    SQLALCHEMY_DATABASE_URI = 'mysql://user:password@db/bank'
    JSONIFY_PRETTYPRINT_REGULAR = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # significantly reduces overhead
    SECRET_KEY = 'SECRET'
