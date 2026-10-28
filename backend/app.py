"""FestPass registration API."""

import os
import socket
from contextlib import closing

import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)

REGNO = os.getenv("REGNO", "NOT-SET")
APP_VERSION = os.getenv("APP_VERSION", "dev")
TABLE_SQL = """
CREATE TABLE IF NOT EXISTS registrations (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    event TEXT NOT NULL,
    created TIMESTAMPTZ NOT NULL DEFAULT now()
)
"""


def connect():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        dbname=os.getenv("DB_NAME", "festpass"),
        user=os.getenv("DB_USER", "festpass"),
        password=os.getenv("DB_PASSWORD", ""),
        connect_timeout=3,
    )


def run_sql(statement, params=(), fetch=False):
    with closing(connect()) as conn:
        with conn.cursor() as cur:
            cur.execute(TABLE_SQL)
            cur.execute(statement, params)
            rows = cur.fetchall() if fetch else None
        conn.commit()
        return rows


@app.errorhandler(psycopg2.Error)
def database_error(_error):
    return jsonify(error="database unavailable"), 503


@app.get("/api/health")
def health():
    try:
        with closing(connect()) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
    except psycopg2.Error:
        database = False
    else:
        database = True

    return jsonify(
        service="festpass-backend",
        regno=REGNO,
        version=APP_VERSION,
        container=socket.gethostname(),
        database=database,
    )


@app.get("/api/registrations")
def registrations():
    rows = run_sql(
        "SELECT id, name, event, created FROM registrations ORDER BY id",
        fetch=True,
    )
    return jsonify(
        registrations=[
            {
                "id": row[0],
                "name": row[1],
                "event": row[2],
                "created_at": row[3].isoformat(),
            }
            for row in rows
        ]
    )


@app.post("/api/registrations")
def add_registration():
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    event = data.get("event")
    if not isinstance(name, str) or not name.strip():
        return jsonify(error="name is required"), 400
    if not isinstance(event, str) or not event.strip():
        return jsonify(error="event is required"), 400

    rows = run_sql(
        "INSERT INTO registrations (name, event) VALUES (%s, %s) "
        "RETURNING id, name, event, created",
        (name.strip(), event.strip()),
        fetch=True,
    )
    row = rows[0]
    return (
        jsonify(
            registration={
                "id": row[0],
                "name": row[1],
                "event": row[2],
                "created_at": row[3].isoformat(),
            }
        ),
        201,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
