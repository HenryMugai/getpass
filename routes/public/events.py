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
    # GET FILTERS
    # ==========================================
    search = request.args.get('search', '').strip()
    category = request.args.get('category', '').strip()

    # ==========================================
    # BASE QUERY
    # ==========================================
    query = """
        SELECT
            e.id,
            e.title,
            e.slug,
            e.description,
            e.category,
            e.venue_name,
            e.venue_address,
            e.county,
            e.event_date,
            e.start_time,
            e.end_time,
            e.banner_image,
            e.is_featured,
            e.views_count,
            e.created_at,

            COALESCE(MIN(t.price), 0) AS starting_price,
            COUNT(t.id) AS ticket_types

        FROM events e

        LEFT JOIN tickets t
            ON e.id = t.event_id
            AND t.is_active = TRUE

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
                OR LOWER(COALESCE(e.venue_name, '')) LIKE LOWER(%s)
                OR LOWER(COALESCE(e.venue_address, '')) LIKE LOWER(%s)
                OR LOWER(COALESCE(e.county, '')) LIKE LOWER(%s)
                OR LOWER(COALESCE(e.description, '')) LIKE LOWER(%s)
            )
        """

        search_term = f"%{search}%"
        params.extend([
            search_term,
            search_term,
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
    # GROUP BY + ORDER BY
    # ==========================================
    query += """
        GROUP BY
            e.id,
            e.title,
            e.slug,
            e.description,
            e.category,
            e.venue_name,
            e.venue_address,
            e.county,
            e.event_date,
            e.start_time,
            e.end_time,
            e.banner_image,
            e.is_featured,
            e.views_count,
            e.created_at

        ORDER BY
            e.is_featured DESC,
            e.event_date ASC,
            e.start_time ASC,
            e.created_at DESC
    """

    # ==========================================
    # EXECUTE QUERY
    # ==========================================
    events = query_db(query, params)

    # ==========================================
    # GET CATEGORIES
    # ==========================================
    categories = query_db("""
        SELECT DISTINCT category
        FROM events
        WHERE status = 'published'
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