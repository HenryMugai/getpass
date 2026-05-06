# routes/admin/agents.py

from flask import (
    render_template,
    request,
    redirect,
    flash
)

from werkzeug.security import generate_password_hash

from database.db import (
    query_db,
    execute_db
)

from . import admin_bp


@admin_bp.route('/agents', methods=['GET', 'POST'])
def agents():

    # =========================================
    # CREATE AGENT
    # =========================================
    if request.method == 'POST':

        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')

        assigned_event = request.form.get('assigned_event')

        # =========================================
        # VALIDATION
        # =========================================
        if not all([
            full_name,
            email,
            password
        ]):

            flash(
                'Please fill all required fields.',
                'error'
            )

            return redirect('/admin/agents')

        # =========================================
        # CHECK EMAIL
        # =========================================
        existing_agent = query_db("""

            SELECT id
            FROM users
            WHERE email = %s

        """, (email,), one=True)

        if existing_agent:

            flash(
                'Email already exists.',
                'error'
            )

            return redirect('/admin/agents')

        # =========================================
        # CREATE AGENT
        # =========================================
        password_hash = generate_password_hash(
            password
        )

        agent_id = execute_db("""

            INSERT INTO users (

                full_name,
                email,
                phone,
                password_hash,
                role

            )

            VALUES (

                %s,
                %s,
                %s,
                %s,
                'agent'

            )

        """, (

            full_name,
            email,
            phone,
            password_hash

        ))

        # =========================================
        # ASSIGN EVENT
        # =========================================
        if assigned_event:

            execute_db("""

                INSERT INTO agent_events (

                    event_id,
                    agent_id

                )

                VALUES (

                    %s,
                    %s

                )

            """, (

                assigned_event,
                agent_id

            ))

        flash(
            'Agent created successfully.',
            'success'
        )

        return redirect('/admin/agents')

    # =========================================
    # SUSPEND AGENT
    # =========================================
    suspend_id = request.args.get('suspend')

    if suspend_id:

        execute_db("""

            UPDATE users
            SET is_active = 0
            WHERE id = %s

        """, (suspend_id,))

        flash(
            'Agent suspended successfully.',
            'success'
        )

        return redirect('/admin/agents')

    # =========================================
    # ACTIVATE AGENT
    # =========================================
    activate_id = request.args.get('activate')

    if activate_id:

        execute_db("""

            UPDATE users
            SET is_active = 1
            WHERE id = %s

        """, (activate_id,))

        flash(
            'Agent activated successfully.',
            'success'
        )

        return redirect('/admin/agents')

    # =========================================
    # EVENTS
    # =========================================
    events = query_db("""

        SELECT
            id,
            title

        FROM events

        WHERE status = 'published'

        ORDER BY start_date ASC

    """)

    # =========================================
    # AGENTS
    # =========================================
    agents = query_db("""

        SELECT

            u.id,
            u.full_name,
            u.email,
            u.phone,
            u.is_active,
            u.last_login,

            e.title AS assigned_event

        FROM users u

        LEFT JOIN agent_events ea
            ON u.id = ea.agent_id

        LEFT JOIN events e
            ON ea.event_id = e.id

        WHERE u.role = 'agent'

        ORDER BY u.created_at DESC

    """)

    return render_template(
        'admin/agents.html',
        agents=agents,
        events=events
    )