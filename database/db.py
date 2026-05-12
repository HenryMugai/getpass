# database/db.py

import psycopg2
from psycopg2.extras import RealDictCursor
from flask import g
from config import DB_CONFIG


def get_db():
    """
    Create or return an existing PostgreSQL connection
    for the current Flask request.
    """
    if 'db' not in g:
        g.db = psycopg2.connect(**DB_CONFIG)
    return g.db


def close_db(e=None):
    """
    Close DB connection after request.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


# =====================================
# QUERY HELPERS
# =====================================

def query_db(query, args=None, one=False):
    """
    Run SELECT queries.

    Returns:
        - one=True  -> single dictionary or None
        - one=False -> list of dictionaries
    """
    conn = get_db()

    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(query, args or ())

        # Fetch all rows as dictionaries
        result = cursor.fetchall()

    if one:
        return result[0] if result else None

    return result


def execute_db(query, args=None):
    """
    Run INSERT / UPDATE / DELETE queries.

    Returns:
        - inserted row ID if available
        - None otherwise
    """
    conn = get_db()

    with conn.cursor() as cursor:
        cursor.execute(query, args or ())

        last_id = None

        # PostgreSQL supports RETURNING id
        # If your INSERT query includes:
        # INSERT INTO table (...) VALUES (...) RETURNING id;
        if cursor.description:
            returned = cursor.fetchone()
            if returned:
                last_id = returned[0]

        conn.commit()

    return last_id