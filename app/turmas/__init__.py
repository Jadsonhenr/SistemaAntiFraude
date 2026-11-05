from flask import Blueprint
turmas_bp = Blueprint("turmas", __name__)
from . import routes
