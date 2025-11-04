# api/__init__.py
from flask import Blueprint
from flask_restful import Api

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)


from . import routes  # noqa: E402,F401
