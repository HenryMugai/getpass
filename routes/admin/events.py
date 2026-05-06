# routes/admin/events.py

from flask import (
    render_template,
    request,
    redirect,
    flash
)

from database.db import (
    query_db,
    execute_db
)

from werkzeug.utils import secure_filename

import os
import uuid

from . import admin_bp


UPLOAD_FOLDER = 'static/uploads/events'


@admin_bp.route('/events', methods=['GET', 'POST'])
def events():

    # =========================================
    # CREATE EVENT
    # =========================================
    if request.method == 'POST':

        title = request.form.get('title')
        slug = request.form.get('slug')
        short_description = request.form.get('short_description')
        description = request.form.get('description')

        category = request.form.get('category')

        venue = request.form.get('venue')
        location = request.form.get('location')

        organiser_id = request.form.get('organiser_id')

        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        ticket_sale_start = request.form.get('ticket_sale_start')
        ticket_sale_end = request.form.get('ticket_sale_end')

        featured = 1 if request.form.get('featured') else 0
        is_free = 1 if request.form.get('is_free') else 0

        max_attendees = request.form.get('max_attendees') or 0

        status = request.form.get('status')

        # =========================================
        # POSTER UPLOAD
        # =========================================
        event_image = None

        image = request.files.get('event_image')

        if image and image.filename != '':

            extension = os.path.splitext(
                image.filename
            )[1]

            filename = f"{uuid.uuid4().hex}{extension}"

            filename = secure_filename(filename)

            os.makedirs(
                UPLOAD_FOLDER,
                exist_ok=True
            )

            save_path = os.path.join(
                UPLOAD_FOLDER,
                filename
            )

            image.save(save_path)

            event_image = f"uploads/events/{filename}"

        # =========================================
        # INSERT EVENT
        # =========================================
        event_id = execute_db("""

            INSERT INTO events (

                organiser_id,
                title,
                slug,
                short_description,
                description,
                category,
                venue,
                location,
                event_image,
                start_date,
                end_date,
                ticket_sale_start,
                ticket_sale_end,
                status,
                featured,
                is_free,
                max_attendees

            )

            VALUES (

                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s

            )

        """, (

            organiser_id,
            title,
            slug,
            short_description,
            description,
            category,
            venue,
            location,
            event_image,
            start_date,
            end_date,
            ticket_sale_start,
            ticket_sale_end,
            status,
            featured,
            is_free,
            max_attendees

        ))

        # =========================================
        # CREATE TICKET
        # =========================================
        ticket_name = request.form.get('ticket_name')
        ticket_price = request.form.get('ticket_price')
        ticket_quantity = request.form.get('ticket_quantity')

        if ticket_name and ticket_price:

            execute_db("""

                INSERT INTO tickets (

                    event_id,
                    name,
                    price,
                    quantity

                )

                VALUES (

                    %s,
                    %s,
                    %s,
                    %s

                )

            """, (

                event_id,
                ticket_name,
                ticket_price,
                ticket_quantity or 0

            ))

        flash(
            'Event created successfully.',
            'success'
        )

        return redirect('/admin/events')

    # =========================================
    # ORGANISERS
    # =========================================
    organisers = query_db("""

        SELECT
            id,
            full_name

        FROM users

        WHERE role = 'organiser'
        AND is_active = 1

        ORDER BY full_name ASC

    """)

    # =========================================
    # EVENTS
    # =========================================
    events = query_db("""

        SELECT

            e.id,
            e.title,
            e.slug,
            e.category,
            e.location,
            e.event_image,
            e.start_date,
            e.status,
            e.featured,

            u.full_name AS organiser_name,

            COUNT(t.id) AS total_ticket_types

        FROM events e

        LEFT JOIN users u
            ON e.organiser_id = u.id

        LEFT JOIN tickets t
            ON e.id = t.event_id

        GROUP BY e.id

        ORDER BY e.created_at DESC

    """)

    return render_template(
        'admin/events.html',
        organisers=organisers,
        events=events
    )