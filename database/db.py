import sqlite3
import os
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "spendly.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    try:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                name          TEXT NOT NULL,
                email         TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at    TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS expenses (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL,
                amount      REAL NOT NULL,
                category    TEXT NOT NULL,
                date        TEXT NOT NULL,
                description TEXT,
                created_at  TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        """)
        conn.commit()
    finally:
        conn.close()


def seed_db():
    conn = get_db()
    try:
        count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        if count > 0:
            return

        password_hash = generate_password_hash("demo123")
        conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            ("Demo User", "demo@spendly.com", password_hash),
        )

        user_id = conn.execute(
            "SELECT id FROM users WHERE email = ?", ("demo@spendly.com",)
        ).fetchone()[0]

        today = date.today()
        expenses = [
            (user_id, 12.50,  "Food",          today.replace(day=1).isoformat(),  "Lunch at cafe"),
            (user_id, 35.00,  "Transport",     today.replace(day=3).isoformat(),  "Monthly bus pass"),
            (user_id, 120.00, "Bills",         today.replace(day=5).isoformat(),  "Electric bill"),
            (user_id, 45.00,  "Health",        today.replace(day=8).isoformat(),  "Pharmacy"),
            (user_id, 15.99,  "Entertainment", today.replace(day=10).isoformat(), "Movie tickets"),
            (user_id, 67.30,  "Shopping",      today.replace(day=12).isoformat(), "New shoes"),
            (user_id, 9.99,   "Other",         today.replace(day=15).isoformat(), "Miscellaneous"),
            (user_id, 22.75,  "Food",          today.replace(day=18).isoformat(), "Grocery run"),
        ]

        conn.executemany(
            "INSERT INTO expenses (user_id, amount, category, date, description) "
            "VALUES (?, ?, ?, ?, ?)",
            expenses,
        )
        conn.commit()
    finally:
        conn.close()


def get_user_by_email(email):
    conn = get_db()
    try:
        return conn.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()
    finally:
        conn.close()


def verify_user(email, password):
    user = get_user_by_email(email)
    if user is None:
        return None
    if not check_password_hash(user["password_hash"], password):
        return None
    return {"id": user["id"], "name": user["name"]}


def create_user(name, email, password):
    password_hash = generate_password_hash(password)
    conn = get_db()
    try:
        cursor = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, password_hash),
        )
        conn.commit()
        return {"id": cursor.lastrowid, "name": name}
    finally:
        conn.close()
