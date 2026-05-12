# routes/public/index.py

from flask import render_template
from database.db import query_db
from . import public_bp


@public_bp.route('/')
def index():
    """
    Homepage route.

    Updated to match the PostgreSQL schema:

    OLD COLUMN NAME      -> NEW COLUMN NAME
    --------------------------------------
    e.location           -> e.venue_name
    e.event_image        -> e.banner_image
    e.start_date         -> e.event_date
    e.featured           -> e.is_featured
    """

    # =========================================
    # FEATURED EVENTS
    # =========================================
    featured_events = query_db("""
        SELECT
            e.id,
            e.title,
            e.slug,

            -- Alias schema columns to match existing template
            e.venue_name AS location,
            e.category,
            e.banner_image AS event_image,
            e.event_date AS start_date,

            MIN(t.price) AS starting_price

        FROM events e

        LEFT JOIN tickets t
            ON e.id = t.event_id

        WHERE e.status = 'published'

        GROUP BY
            e.id,
            e.title,
            e.slug,
            e.venue_name,
            e.category,
            e.banner_image,
            e.event_date,
            e.is_featured

        ORDER BY
            e.is_featured DESC,
            e.event_date ASC

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

    # =========================================
    # RENDER TEMPLATE
    # =========================================
    return render_template(
        'public/index.html',
        featured_events=featured_events,
        total_events=total_events['total'] if total_events else 0,
        total_tickets=total_tickets['total'] if total_tickets else 0
    )