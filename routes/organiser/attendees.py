# routes/organiser/attendees.py

from flask import (
    render_template,
    session,
    redirect,
    request,
    Response
)

import csv
import io

from database.db import query_db

from . import organiser_bp


@organiser_bp.route('/attendees')
def attendees():

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
            full_name

        FROM users

        WHERE id = %s
        AND role = 'organiser'

    """, (organiser_id,), one=True)

    if not organiser:

        return redirect('/auth/login')

    # =========================================
    # FILTERS
    # =========================================
    selected_event = request.args.get('event')
    search = request.args.get('search', '').strip()

    # =========================================
    # EVENTS
    # =========================================
    events = query_db("""

        SELECT

            id,
            title

        FROM events

        WHERE organiser_id = %s

        ORDER BY start_date DESC

    """, (organiser_id,))

    # =========================================
    # ATTENDEES QUERY
    # =========================================
    query = """

        SELECT

            a.id,
            a.full_name,
            a.email,
            a.phone,
            a.ticket_code,
            a.checkin_status,
            a.checked_in_at,
            a.created_at,

            t.ticket_name,

            e.title AS event_title

        FROM attendees a

        INNER JOIN events e
            ON a.event_id = e.id

        LEFT JOIN tickets t
            ON a.ticket_id = t.id

        WHERE e.organiser_id = %s

    """

    params = [organiser_id]

    # =========================================
    # EVENT FILTER
    # =========================================
    if selected_event:

        query += """

            AND e.id = %s

        """

        params.append(selected_event)

    # =========================================
    # SEARCH FILTER
    # =========================================
    if search:

        query += """

            AND (

                a.full_name LIKE %s
                OR a.email LIKE %s
                OR a.ticket_code LIKE %s

            )

        """

        search_term = f"%{search}%"

        params.extend([
            search_term,
            search_term,
            search_term
        ])

    query += """

        ORDER BY a.created_at DESC

    """

    attendees = query_db(
        query,
        tuple(params)
    )

    # =========================================
    # EXPORT CSV
    # =========================================
    export = request.args.get('export')

    if export == 'csv':

        output = io.StringIO()

        writer = csv.writer(output)

        writer.writerow([

            'Full Name',
            'Email',
            'Phone',
            'Ticket Code',
            'Ticket Type',
            'Event',
            'Checked In',
            'Checked In At',
            'Registered At'

        ])

        for attendee in attendees:

            writer.writerow([

                attendee['full_name'],
                attendee['email'],
                attendee['phone'],
                attendee['ticket_code'],
                attendee['ticket_name'],
                attendee['event_title'],
                'Yes' if attendee['checkin_status'] else 'No',
                attendee['checked_in_at'],
                attendee['created_at']

            ])

        output.seek(0)

        return Response(

            output.getvalue(),

            mimetype='text/csv',

            headers={

                'Content-Disposition':
                'attachment; filename=attendees.csv'

            }

        )

    # =========================================
    # ANALYTICS
    # =========================================
    total_attendees = len(attendees)

    checked_in = len([
        attendee for attendee in attendees
        if attendee['checkin_status'] == 1
    ])

    pending = total_attendees - checked_in

    attendance_rate = 0

    if total_attendees > 0:

        attendance_rate = round(
            (checked_in / total_attendees) * 100
        )

    # =========================================
    # PAGE RENDER
    # =========================================
    return render_template(

        'organiser/attendees.html',

        organiser=organiser,

        attendees=attendees,
        events=events,

        selected_event=selected_event,
        search=search,

        total_attendees=total_attendees,
        checked_in=checked_in,
        pending=pending,
        attendance_rate=attendance_rate

    )