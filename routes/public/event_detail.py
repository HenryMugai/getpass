# routes/public/event_detail.py

from flask import render_template
from . import public_bp

@public_bp.route('/event/<int:event_id>')
def event_detail(event_id):
    return render_template('public/event_detail.html', event_id=event_id)