from flask import Blueprint
analises_bp = Blueprint("analises", __name__)
from . import routes
