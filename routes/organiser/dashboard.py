# routes/organiser/dashboard.py

from flask import (
    render_template,
    session,
    redirect
)

from database.db import query_db

from . import organiser_bp


@organiser_bp.route('/')
def dashboard():

    # =========================================
    # AUTH CHECK
    # =========================================
    if 'user_id' not in session:

        return redirect('/auth/login')

    organiser_id = session['user_id']

    # =========================================
    # ORGANISER
    # =========================================
    organiser = query_db("""

        SELECT
            id,
            full_name,
            email

        FROM users

        WHERE id = %s
        AND role = 'organiser'

    """, (organiser_id,), one=True)

    if not organiser:

        return redirect('/auth/login')

    # =========================================
    # TOTAL EVENTS
    # =========================================
    total_events = query_db("""

        SELECT COUNT(*) AS total

        FROM events

        WHERE organiser_id = %s

    """, (organiser_id,), one=True)

    # =========================================
    # PUBLISHED EVENTS
    # =========================================
    published_events = query_db("""

        SELECT COUNT(*) AS total

        FROM events

        WHERE organiser_id = %s
        AND status = 'published'

    """, (organiser_id,), one=True)

    # =========================================
    # TOTAL ATTENDEES
    # =========================================
    total_attendees = query_db("""

        SELECT COUNT(a.id) AS total

        FROM attendees a

        INNER JOIN events e
            ON a.event_id = e.id

        WHERE e.organiser_id = %s

    """, (organiser_id,), one=True)

    # =========================================
    # CHECKED IN
    # =========================================
    checked_in = query_db("""

        SELECT COUNT(a.id) AS total

        FROM attendees a

        INNER JOIN events e
            ON a.event_id = e.id

        WHERE e.organiser_id = %s
        AND a.checkin_status = 1

    """, (organiser_id,), one=True)

    # =========================================
    # RECENT EVENTS
    # =========================================
    recent_events = query_db("""

        SELECT

            id,
            title,
            location,
            event_image,
            start_date,
            status

        FROM events

        WHERE organiser_id = %s

        ORDER BY created_at DESC

        LIMIT 5

    """, (organiser_id,))

    # =========================================
    # RECENT ATTENDEES
    # =========================================
    recent_attendees = query_db("""

        SELECT

            a.full_name,
            a.email,
            a.phone,
            a.ticket_code,
            a.checkin_status,

            e.title AS event_title

        FROM attendees a

        INNER JOIN events e
            ON a.event_id = e.id

        WHERE e.organiser_id = %s

        ORDER BY a.created_at DESC

        LIMIT 8

    """, (organiser_id,))

    return render_template(

        'organiser/dashboard.html',

        organiser=organiser,

        total_events=total_events['total'],
        published_events=published_events['total'],
        total_attendees=total_attendees['total'],
        checked_in=checked_in['total'],

        recent_events=recent_events,
        recent_attendees=recent_attendees

    )