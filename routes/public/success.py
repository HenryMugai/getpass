# routes/public/success.py

from flask import render_template
from . import public_bp

@public_bp.route('/success')
def success():
    return render_template('public/success.html')