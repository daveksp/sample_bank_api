import os
import uuid

from flask import g
from flask import request


def request_ids():
    """
    Return an id that lasts the life of the request, or create one if
    this is the first time the value is being returned
    :return: tuple(new_request_id, original_request_id)
    """
    if getattr(g, 'request_id', None):
        return g.request_id, g.get('original_request_id')

    g.request_id = _generate_request_id()
    g.original_request_id = request.headers.get('Request-Id')

    return g.request_id, g.original_request_id


def _generate_request_id():
    """Generate a new request ID"""
    return uuid.uuid4()


def project_path(subpath=None):
    """
    Get the absolute path of the project

    :param subpath: A subpath within the project.  If omitted,
    return the project root
    """
    p = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if subpath:
        if isinstance(subpath, str):
            subpath = (subpath,)
        parts = (p,) + tuple(subpath)
        p = os.path.sep.join(parts)
    return p
