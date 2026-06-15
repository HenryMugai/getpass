<<<<<<< HEAD
# routes/public/events.py

=======
>>>>>>> f941ac10000991d49d84309a786eb4d37c52228f
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
<<<<<<< HEAD
    # GET FILTER PARAMETERS
=======
    # GET FILTERS
>>>>>>> f941ac10000991d49d84309a786eb4d37c52228f
    # ==========================================
    search = request.args.get('search', '').strip()
    category = request.args.get('category', '').strip()

    # ==========================================
<<<<<<< HEAD
    # BUILD EVENTS QUERY
=======
    # BASE QUERY
>>>>>>> f941ac10000991d49d84309a786eb4d37c52228f
    # ==========================================
    query = """
        SELECT
            e.id,
            e.title,
            e.slug,
<<<<<<< HEAD
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
=======
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
>>>>>>> f941ac10000991d49d84309a786eb4d37c52228f

        FROM events e

        LEFT JOIN tickets t
            ON e.id = t.event_id
<<<<<<< HEAD
            AND t.status = 'active'
=======
            AND t.is_active = TRUE
>>>>>>> f941ac10000991d49d84309a786eb4d37c52228f

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
<<<<<<< HEAD
                OR LOWER(COALESCE(e.venue, '')) LIKE LOWER(%s)
                OR LOWER(COALESCE(e.short_description, '')) LIKE LOWER(%s)
=======
                OR LOWER(COALESCE(e.venue_name, '')) LIKE LOWER(%s)
                OR LOWER(COALESCE(e.venue_address, '')) LIKE LOWER(%s)
                OR LOWER(COALESCE(e.county, '')) LIKE LOWER(%s)
                OR LOWER(COALESCE(e.description, '')) LIKE LOWER(%s)
>>>>>>> f941ac10000991d49d84309a786eb4d37c52228f
            )
        """

        search_term = f"%{search}%"
        params.extend([
            search_term,
            search_term,
            search_term,
<<<<<<< HEAD
=======
            search_term,
            search_term,
>>>>>>> f941ac10000991d49d84309a786eb4d37c52228f
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
<<<<<<< HEAD
    # GROUPING AND ORDERING
    # ==========================================
    query += """
        GROUP BY
            e.id

        ORDER BY
            e.featured DESC,
            e.start_date ASC,
=======
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
>>>>>>> f941ac10000991d49d84309a786eb4d37c52228f
            e.created_at DESC
    """

    # ==========================================
<<<<<<< HEAD
    # EXECUTE EVENTS QUERY
=======
    # EXECUTE QUERY
>>>>>>> f941ac10000991d49d84309a786eb4d37c52228f
    # ==========================================
    events = query_db(query, params)

    # ==========================================
<<<<<<< HEAD
    # GET AVAILABLE CATEGORIES
=======
    # GET CATEGORIES
>>>>>>> f941ac10000991d49d84309a786eb4d37c52228f
    # ==========================================
    categories = query_db("""
        SELECT DISTINCT category
        FROM events
<<<<<<< HEAD
        WHERE
            status = 'published'
            AND category IS NOT NULL
            AND category <> ''
=======
        WHERE status = 'published'
          AND category IS NOT NULL
          AND category <> ''
>>>>>>> f941ac10000991d49d84309a786eb4d37c52228f
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