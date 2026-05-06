# database/db.py

import mysql.connector
from flask import g
from config import DB_CONFIG


def get_db():
    """
    Create or return an existing DB connection for the request
    """
    if 'db' not in g:
        g.db = mysql.connector.connect(**DB_CONFIG)
    return g.db


def close_db(e=None):
    """
    Close DB connection after request
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


# ================================
# QUERY HELPERS
# ================================

def query_db(query, args=None, one=False):
    """
    Run SELECT queries
    """
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(query, args or ())
    result = cursor.fetchall()

    cursor.close()

    return (result[0] if result else None) if one else result


def execute_db(query, args=None):
    """
    Run INSERT / UPDATE / DELETE
    """
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(query, args or ())
    conn.commit()

    last_id = cursor.lastrowid

    cursor.close()

    return last_id