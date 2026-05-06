# routes/admin/dashboard.py

from flask import render_template
from database.db import query_db
from . import admin_bp


@admin_bp.route('/')
def dashboard():

    # =========================================
    # TOTAL EVENTS
    # =========================================
    total_events = query_db("""

        SELECT COUNT(*) AS total
        FROM events

    """, one=True)

    # =========================================
    # PUBLISHED EVENTS
    # =========================================
    published_events = query_db("""

        SELECT COUNT(*) AS total
        FROM events
        WHERE status = 'published'

    """, one=True)

    # =========================================
    # TOTAL USERS
    # =========================================
    total_users = query_db("""

        SELECT COUNT(*) AS total
        FROM users

    """, one=True)

    # =========================================
    # TOTAL AGENTS
    # =========================================
    total_agents = query_db("""

        SELECT COUNT(*) AS total
        FROM users
        WHERE role = 'agent'

    """, one=True)

    # =========================================
    # RECENT EVENTS
    # =========================================
    recent_events = query_db("""

        SELECT
            title,
            category,
            location,
            start_date,
            status

        FROM events

        ORDER BY created_at DESC

        LIMIT 5

    """)

    return render_template(
        'admin/dashboard.html',
        total_events=total_events['total'] if total_events else 0,
        published_events=published_events['total'] if published_events else 0,
        total_users=total_users['total'] if total_users else 0,
        total_agents=total_agents['total'] if total_agents else 0,
        recent_events=recent_events
    )