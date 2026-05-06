# routes/public/__init__.py

from flask import Blueprint

public_bp = Blueprint(
    'public',
    __name__,
    template_folder='../../templates/public'
)

from . import index, events, event_detail, checkout, success