# routes/public/index.py

from flask import render_template
from database.db import query_db
from . import public_bp


@public_bp.route('/')
def index():

    # =========================================
    # FEATURED EVENTS
    # =========================================
    featured_events = query_db("""

        SELECT
            e.id,
            e.title,
            e.slug,
            e.location,
            e.category,
            e.event_image,
            e.start_date,

            MIN(t.price) AS starting_price

        FROM events e

        LEFT JOIN tickets t
            ON e.id = t.event_id

        WHERE e.status = 'published'

        GROUP BY e.id

        ORDER BY
            e.featured DESC,
            e.start_date ASC

        LIMIT 6

    """)

    # =========================================
    # PLATFORM STATS
    # =========================================
    total_events = query_db("""

        SELECT COUNT(*) AS total
        FROM events
        WHERE status = 'published'

    """, one=True)

    total_tickets = query_db("""

        SELECT COUNT(*) AS total
        FROM attendees

    """, one=True)

    return render_template(
        'public/index.html',
        featured_events=featured_events,
        total_events=total_events['total'] if total_events else 0,
        total_tickets=total_tickets['total'] if total_tickets else 0
    )