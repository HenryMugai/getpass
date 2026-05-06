# routes/admin/users.py

from flask import (
    render_template,
    request,
    redirect,
    flash,
    url_for
)

from werkzeug.security import generate_password_hash

from database.db import (
    query_db,
    execute_db
)

from . import admin_bp


@admin_bp.route('/users', methods=['GET', 'POST'])
def users():

    # =========================================
    # CREATE USER
    # =========================================
    if request.method == 'POST':

        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        role = request.form.get('role')

        # =========================================
        # VALIDATION
        # =========================================
        if not all([
            full_name,
            email,
            password,
            role
        ]):

            flash(
                'Please fill all required fields.',
                'error'
            )

            return redirect('/admin/users')

        # =========================================
        # CHECK EMAIL
        # =========================================
        existing_user = query_db("""

            SELECT id
            FROM users
            WHERE email = %s

        """, (email,), one=True)

        if existing_user:

            flash(
                'Email already exists.',
                'error'
            )

            return redirect('/admin/users')

        # =========================================
        # HASH PASSWORD
        # =========================================
        password_hash = generate_password_hash(
            password
        )

        # =========================================
        # INSERT USER
        # =========================================
        execute_db("""

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
                %s

            )

        """, (

            full_name,
            email,
            phone,
            password_hash,
            role

        ))

        flash(
            'User created successfully.',
            'success'
        )

        return redirect('/admin/users')

    # =========================================
    # SUSPEND USER
    # =========================================
    suspend_id = request.args.get('suspend')

    if suspend_id:

        execute_db("""

            UPDATE users
            SET is_active = 0
            WHERE id = %s

        """, (suspend_id,))

        flash(
            'User suspended successfully.',
            'success'
        )

        return redirect('/admin/users')

    # =========================================
    # ACTIVATE USER
    # =========================================
    activate_id = request.args.get('activate')

    if activate_id:

        execute_db("""

            UPDATE users
            SET is_active = 1
            WHERE id = %s

        """, (activate_id,))

        flash(
            'User activated successfully.',
            'success'
        )

        return redirect('/admin/users')

    # =========================================
    # GET USERS
    # =========================================
    users = query_db("""

        SELECT

            id,
            full_name,
            email,
            phone,
            role,
            is_verified,
            is_active,
            last_login,
            created_at

        FROM users

        ORDER BY created_at DESC

    """)

    return render_template(
        'admin/users.html',
        users=users
    )