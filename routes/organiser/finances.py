# routes/organiser/finances.py

from flask import (
    render_template,
    session,
    redirect
)

from database.db import query_db

from . import organiser_bp


@organiser_bp.route('/finances')
def finances():

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
    # EVENT REVENUE BREAKDOWN
    # =========================================
    event_finances = query_db("""

        SELECT

            e.id,
            e.title,
            e.event_image,
            e.status,

            COUNT(DISTINCT a.id) AS tickets_sold,

            IFNULL(SUM(t.price),0) AS gross_revenue

        FROM events e

        LEFT JOIN attendees a
            ON e.id = a.event_id

        LEFT JOIN tickets t
            ON a.ticket_id = t.id

        WHERE e.organiser_id = %s

        GROUP BY e.id

        ORDER BY gross_revenue DESC

    """, (organiser_id,))

    # =========================================
    # CALCULATIONS
    # =========================================
    gross_revenue = 0
    total_fees = 0
    net_revenue = 0
    total_tickets = 0

    for event in event_finances:

        gross = float(event['gross_revenue'])

        fee = gross * 0.07

        net = gross - fee

        event['platform_fee'] = round(fee, 2)
        event['net_revenue'] = round(net, 2)

        gross_revenue += gross
        total_fees += fee
        net_revenue += net

        total_tickets += event['tickets_sold']

    # =========================================
    # RECENT SALES
    # =========================================
    recent_sales = query_db("""

        SELECT

            a.full_name,
            a.ticket_code,
            a.created_at,

            e.title AS event_title,

            t.ticket_name,
            t.price

        FROM attendees a

        INNER JOIN events e
            ON a.event_id = e.id

        LEFT JOIN tickets t
            ON a.ticket_id = t.id

        WHERE e.organiser_id = %s

        ORDER BY a.created_at DESC

        LIMIT 10

    """, (organiser_id,))

    # =========================================
    # PAGE RENDER
    # =========================================
    return render_template(

        'organiser/finances.html',

        organiser=organiser,

        gross_revenue=round(gross_revenue, 2),
        total_fees=round(total_fees, 2),
        net_revenue=round(net_revenue, 2),
        total_tickets=total_tickets,

        event_finances=event_finances,
        recent_sales=recent_sales

    )