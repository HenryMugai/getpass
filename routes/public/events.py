# routes/public/events.py

from flask import render_template
from database.db import query_db
from . import public_bp


@public_bp.route('/events')
def events():

    # =========================================
    # GET PUBLISHED EVENTS
    # =========================================
    events = query_db("""

        SELECT
            e.id,
            e.title,
            e.slug,
            e.location,
            e.event_image,
            e.start_date,
            e.category,
            e.featured,

            MIN(t.price) AS starting_price

        FROM events e

        LEFT JOIN tickets t
            ON e.id = t.event_id

        WHERE e.status = 'published'

        GROUP BY e.id

        ORDER BY
            e.featured DESC,
            e.start_date ASC

    """)

    return render_template(
        'public/events.html',
        events=events
    )