# routes/public/events.py

from flask import render_template, request
from database.db import query_db
from . import public_bp

@public_bp.route('/events')
def events():
    """
    Public events listing page.
    Displays all published events with optional
    search and category filtering.
    """

    # ==========================================
    # GET FILTER PARAMETERS
    # ==========================================
    search = request.args.get('search', '').strip()
    category = request.args.get('category', '').strip()

    # ==========================================
    # BUILD EVENTS QUERY
    # ==========================================
    query = """
        SELECT
            e.id,
            e.title,
            e.slug,
            e.short_description,
            e.description,
            e.category,
            e.venue,
            e.event_image,
            e.start_date,
            e.end_date,
            e.featured,
            e.is_free,
            e.views_count,

            COALESCE(MIN(t.price), 0) AS starting_price

        FROM events e

        LEFT JOIN tickets t
            ON e.id = t.event_id
            AND t.status = 'active'

        WHERE e.status = 'published'
    """

    params = []

    # ==========================================
    # SEARCH FILTER
    # ==========================================
    if search:
        query += """
            AND (
                LOWER(e.title) LIKE LOWER(%s)
                OR LOWER(COALESCE(e.category, '')) LIKE LOWER(%s)
                OR LOWER(COALESCE(e.venue, '')) LIKE LOWER(%s)
                OR LOWER(COALESCE(e.short_description, '')) LIKE LOWER(%s)
            )
        """

        search_term = f"%{search}%"
        params.extend([
            search_term,
            search_term,
            search_term,
            search_term
        ])

    # ==========================================
    # CATEGORY FILTER
    # ==========================================
    if category:
        query += """
            AND LOWER(COALESCE(e.category, '')) = LOWER(%s)
        """
        params.append(category)

    # ==========================================
    # GROUPING AND ORDERING
    # ==========================================
    query += """
        GROUP BY
            e.id

        ORDER BY
            e.featured DESC,
            e.start_date ASC,
            e.created_at DESC
    """

    # ==========================================
    # EXECUTE EVENTS QUERY
    # ==========================================
    events = query_db(query, params)

    # ==========================================
    # GET AVAILABLE CATEGORIES
    # ==========================================
    categories = query_db("""
        SELECT DISTINCT category
        FROM events
        WHERE
            status = 'published'
            AND category IS NOT NULL
            AND category <> ''
        ORDER BY category ASC
    """)

    # ==========================================
    # RENDER TEMPLATE
    # ==========================================
    return render_template(
        'public/events.html',
        events=events,
        categories=categories,
        search=search,
        selected_category=category
    )