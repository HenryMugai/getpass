# routes/organiser/__init__.py

from flask import Blueprint

organiser_bp = Blueprint(
    'organiser',
    __name__,
    template_folder='../../templates/organiser'
)

from . import dashboard, events, attendees, finances