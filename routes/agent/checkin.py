# routes/agent/checkin.py

from flask import (
    render_template,
    request,
    session,
    redirect,
    flash
)

from database.db import (
    query_db,
    execute_db
)

from . import agent_bp


@agent_bp.route('/checkin', methods=['GET', 'POST'])
def checkin():

    # =========================================
    # AUTH
    # =========================================
    if 'user_id' not in session:

        return redirect('/auth/login')

    if session.get('role') != 'agent':

        return redirect('/auth/login')

    agent_id = session['user_id']

    # =========================================
    # EVENT ID
    # =========================================
    event_id = request.args.get('event_id')

    if not event_id:

        flash('No event selected.', 'error')

        return redirect('/agent')

    # =========================================
    # VALIDATE EVENT ASSIGNMENT
    # =========================================
    event = query_db("""

        SELECT

            e.id,
            e.title,
            e.location,
            e.venue,
            e.start_date,
            e.event_image

        FROM events e

        INNER JOIN agent_events ae
            ON e.id = ae.event_id

        WHERE ae.agent_id = %s
        AND e.id = %s

        LIMIT 1

    """, (agent_id, event_id), one=True)

    if not event:

        flash('Unauthorized event access.', 'error')

        return redirect('/agent')

    # =========================================
    # LOCK FUTURE EVENTS
    # =========================================
    event_day = event['start_date'].date()

    today = query_db("SELECT CURDATE() AS today", one=True)

    if str(event_day) != str(today['today']):

        flash(
            'Attendee access unlocks on the official event day.',
            'error'
        )

        return redirect('/agent')

    # =========================================
    # LIVE STATS
    # =========================================
    stats = query_db("""

        SELECT

            COUNT(*) AS total_attendees,

            SUM(
                CASE
                    WHEN checkin_status = 1
                    THEN 1
                    ELSE 0
                END
            ) AS checked_in

        FROM attendees

        WHERE event_id = %s

    """, (event_id,), one=True)

    # =========================================
    # RECENT CHECKINS
    # =========================================
    recent_checkins = query_db("""

        SELECT

            a.full_name,
            a.ticket_code,
            a.checked_in_at,

            t.ticket_name

        FROM attendees a

        LEFT JOIN tickets t
            ON a.ticket_id = t.id

        WHERE a.event_id = %s
        AND a.checkin_status = 1

        ORDER BY a.checked_in_at DESC

        LIMIT 10

    """, (event_id,))

    # =========================================
    # CHECKIN LOGIC
    # =========================================
    attendee = None
    validation_status = None

    if request.method == 'POST':

        ticket_code = request.form.get('ticket_code')

        if ticket_code:

            attendee = query_db("""

                SELECT

                    a.id,
                    a.full_name,
                    a.email,
                    a.phone,
                    a.ticket_code,
                    a.checkin_status,
                    a.checked_in_at,

                    t.ticket_name

                FROM attendees a

                LEFT JOIN tickets t
                    ON a.ticket_id = t.id

                WHERE a.ticket_code = %s
                AND a.event_id = %s

                LIMIT 1

            """, (ticket_code, event_id), one=True)

            # =========================================
            # INVALID TICKET
            # =========================================
            if not attendee:

                validation_status = 'invalid'

            # =========================================
            # ALREADY USED
            # =========================================
            elif attendee['checkin_status'] == 1:

                validation_status = 'used'

            # =========================================
            # VALID TICKET
            # =========================================
            else:

                execute_db("""

                    UPDATE attendees

                    SET
                        checkin_status = 1,
                        checked_in_at = NOW()

                    WHERE id = %s

                """, (attendee['id'],))

                attendee['checkin_status'] = 1

                validation_status = 'approved'

    # =========================================
    # PAGE RENDER
    # =========================================
    return render_template(

        'agent/checkin.html',

        event=event,

        stats=stats,

        recent_checkins=recent_checkins,

        attendee=attendee,

        validation_status=validation_status

    )