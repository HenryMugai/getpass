# routes/agent/dashboard.py

from flask import (
    render_template,
    session,
    redirect
)

from database.db import query_db

from . import agent_bp


@agent_bp.route('/')
def dashboard():

    # =========================================
    # AUTH CHECK
    # =========================================
    if 'user_id' not in session:

        return redirect('/auth/login')

    if session.get('role') != 'agent':

        return redirect('/auth/login')

    agent_id = session['user_id']

    # =========================================
    # AGENT INFO
    # =========================================
    agent = query_db("""

        SELECT
            id,
            full_name,
            email

        FROM users

        WHERE id = %s
        AND role = 'agent'

    """, (agent_id,), one=True)

    if not agent:

        return redirect('/auth/login')

    # =========================================
    # TODAY ACTIVE EVENTS
    # =========================================
    today_events = query_db("""

        SELECT

            e.id,
            e.title,
            e.location,
            e.venue,
            e.start_date,
            e.end_date,
            e.event_image,
            e.status,

            COUNT(DISTINCT a.id) AS attendees_count,

            SUM(

                CASE

                    WHEN a.checkin_status = 1
                    THEN 1

                    ELSE 0

                END

            ) AS checked_in

        FROM events e

        INNER JOIN agent_events ae
            ON e.id = ae.event_id

        LEFT JOIN attendees a
            ON e.id = a.event_id

        WHERE ae.agent_id = %s

        AND DATE(e.start_date) = CURDATE()

        GROUP BY e.id

        ORDER BY e.start_date ASC

    """, (agent_id,))

    # =========================================
    # UPCOMING EVENTS
    # =========================================
    upcoming_events = query_db("""

        SELECT

            e.id,
            e.title,
            e.location,
            e.venue,
            e.start_date,
            e.event_image,
            e.status

        FROM events e

        INNER JOIN agent_events ae
            ON e.id = ae.event_id

        WHERE ae.agent_id = %s

        AND DATE(e.start_date) > CURDATE()

        ORDER BY e.start_date ASC

    """, (agent_id,))

    # =========================================
    # RECENT CHECKINS
    # =========================================
    recent_checkins = query_db("""

        SELECT

            a.full_name,
            a.ticket_code,
            a.checked_in_at,

            t.ticket_name,

            e.title AS event_title

        FROM attendees a

        INNER JOIN events e
            ON a.event_id = e.id

        LEFT JOIN tickets t
            ON a.ticket_id = t.id

        INNER JOIN agent_events ae
            ON e.id = ae.event_id

        WHERE ae.agent_id = %s
        AND a.checkin_status = 1

        ORDER BY a.checked_in_at DESC

        LIMIT 8

    """, (agent_id,))

    # =========================================
    # PAGE RENDER
    # =========================================
    return render_template(

        'agent/dashboard.html',

        agent=agent,

        today_events=today_events,
        upcoming_events=upcoming_events,

        recent_checkins=recent_checkins

    )