# routes/organiser/events.py

from flask import (
    render_template,
    session,
    redirect,
    request,
    flash
)

from database.db import (
    query_db,
    execute_db
)

from . import organiser_bp


@organiser_bp.route('/events', methods=['GET', 'POST'])
def events():

    # =========================================
    # AUTH CHECK
    # =========================================
    if 'user_id' not in session:

        return redirect('/auth/login')

    organiser_id = session['user_id']

    # =========================================
    # VALIDATE ORGANISER
    # =========================================
    organiser = query_db("""

        SELECT
            id,
            full_name

        FROM users

        WHERE id = %s
        AND role = 'organiser'

    """, (organiser_id,), one=True)

    if not organiser:

        return redirect('/auth/login')

    # =========================================
    # UPDATE EVENT POSTER
    # =========================================
    if request.method == 'POST':

        event_id = request.form.get('event_id')
        event_image = request.form.get('event_image')

        if event_id and event_image:

            execute_db("""

                UPDATE events

                SET event_image = %s

                WHERE id = %s
                AND organiser_id = %s

            """, (

                event_image,
                event_id,
                organiser_id

            ))

            flash(
                'Event poster updated successfully.',
                'success'
            )

            return redirect('/organiser/events')

    # =========================================
    # ORGANISER EVENTS
    # =========================================
    events = query_db("""

        SELECT

            e.id,
            e.title,
            e.slug,
            e.location,
            e.event_image,
            e.start_date,
            e.status,
            e.views_count,

            COUNT(DISTINCT a.id) AS attendees_count,

            COUNT(
                DISTINCT CASE
                    WHEN a.checkin_status = 1
                    THEN a.id
                END
            ) AS checked_in_count,

            COUNT(DISTINCT t.id) AS ticket_types,

            IFNULL(
                SUM(t.quantity),
                0
            ) AS total_ticket_quantity,

            COUNT(DISTINCT a.id) AS total_tickets_sold

        FROM events e

        LEFT JOIN attendees a
            ON e.id = a.event_id

        LEFT JOIN tickets t
            ON e.id = t.event_id

        WHERE e.organiser_id = %s

        GROUP BY e.id

        ORDER BY e.start_date DESC

    """, (organiser_id,))

    # =========================================
    # PAGE RENDER
    # =========================================
    return render_template(

        'organiser/events.html',

        organiser=organiser,
        events=events

    )