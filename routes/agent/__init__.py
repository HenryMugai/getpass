# routes/agent/__init__.py

from flask import Blueprint

agent_bp = Blueprint(
    'agent',
    __name__,
    template_folder='../../templates/agent'
)

from . import dashboard, checkin