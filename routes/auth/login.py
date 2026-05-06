# routes/auth/login.py

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from werkzeug.security import check_password_hash

from database.db import query_db, execute_db
from . import auth_bp


# =========================================
# LOGIN
# =========================================
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    # =========================================
    # IF USER ALREADY LOGGED IN
    # =========================================
    if session.get('user_id'):

        role = session.get('role')

        if role == 'admin':
            return redirect('/admin/')

        elif role == 'organiser':
            return redirect('/organiser/')

        elif role == 'agent':
            return redirect('/agent/')

        return redirect('/')

    # =========================================
    # LOGIN SUBMIT
    # =========================================
    if request.method == 'POST':

        email = request.form.get(
            'email',
            ''
        ).strip()

        password = request.form.get(
            'password',
            ''
        ).strip()

        # =========================================
        # VALIDATION
        # =========================================
        if not email or not password:

            flash(
                'Authentication failed.',
                'error'
            )

            return redirect(
                url_for('auth.login')
            )

        try:

            # =========================================
            # FIND USER
            # =========================================
            user = query_db("""

                SELECT
                    id,
                    full_name,
                    email,
                    password_hash,
                    role,
                    is_active

                FROM users

                WHERE email = %s

                LIMIT 1

            """, (email,), one=True)

            # =========================================
            # USER NOT FOUND
            # =========================================
            if not user:

                flash(
                    'Authentication failed.',
                    'error'
                )

                return redirect(
                    url_for('auth.login')
                )

            # =========================================
            # ACCOUNT INACTIVE
            # =========================================
            if not user['is_active']:

                flash(
                    'Your account is inactive.',
                    'error'
                )

                return redirect(
                    url_for('auth.login')
                )

            # =========================================
            # PASSWORD CHECK
            # =========================================
            password_valid = check_password_hash(
                user['password_hash'],
                password
            )

            if not password_valid:

                flash(
                    'Authentication failed.',
                    'error'
                )

                return redirect(
                    url_for('auth.login')
                )

            # =========================================
            # CREATE SESSION
            # =========================================
            session['user_id'] = user['id']
            session['user_name'] = user['full_name']
            session['user_email'] = user['email']
            session['role'] = user['role']

            # =========================================
            # UPDATE LAST LOGIN
            # =========================================
            execute_db("""

                UPDATE users
                SET last_login = NOW()
                WHERE id = %s

            """, (user['id'],))

            # =========================================
            # ROLE REDIRECTS
            # =========================================
            if user['role'] == 'admin':

                return redirect('/admin/')

            elif user['role'] == 'organiser':

                return redirect('/organiser/')

            elif user['role'] == 'agent':

                return redirect('/agent/')

            # =========================================
            # DEFAULT
            # =========================================
            return redirect('/')

        except Exception:

            flash(
                'Authentication failed.',
                'error'
            )

            return redirect(
                url_for('auth.login')
            )

    return render_template(
        'auth/login.html'
    )


# =========================================
# LOGOUT
# =========================================
@auth_bp.route('/logout')
def logout():

    session.clear()

    flash(
        'You have been logged out.',
        'success'
    )

    return redirect(
        url_for('auth.login')
    )