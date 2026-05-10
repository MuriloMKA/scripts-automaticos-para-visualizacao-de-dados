from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Generator, Iterable

from ..core.config import get_settings


SETTINGS = get_settings()
DB_PATH = SETTINGS.database_path


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _ensure_parent_directory() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)


@contextmanager
def get_connection() -> Generator[sqlite3.Connection, None, None]:
    _ensure_parent_directory()
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()


def initialize_database() -> None:
    with get_connection() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS generated_scripts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                conversation_id TEXT NOT NULL,
                question TEXT NOT NULL,
                output_format TEXT NOT NULL,
                reply TEXT NOT NULL,
                script TEXT NOT NULL,
                language TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );

            CREATE INDEX IF NOT EXISTS idx_chat_messages_conversation_id
                ON chat_messages (conversation_id, id DESC);

            CREATE INDEX IF NOT EXISTS idx_generated_scripts_created_at
                ON generated_scripts (created_at DESC);
                
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL,
                full_name TEXT,
                role TEXT DEFAULT 'user',
                created_at TEXT NOT NULL
            );
            """
        )


def ensure_default_user() -> None:
    """Create default admin user if it doesn't exist"""
    from ..core.security import hash_password
    
    default_email = "admin@klabin.com.br"
    with get_connection() as connection:
        existing_user = connection.execute("SELECT * FROM users WHERE email = ?", (default_email,)).fetchone()
        
        if not existing_user:
            hashed_pw = hash_password("admin")
            connection.execute(
                "INSERT INTO users (email, hashed_password, full_name, created_at) VALUES (?,?,?,?)",
                (default_email, hashed_pw, "Admin", _now_iso())
            )

def get_user_by_email(email: str):
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        return dict(row) if row else None

def create_user(email: str, hashed_pw: str, name: str):
    with get_connection() as conn:
        conn.execute("INSERT INTO users (email, hashed_password, full_name, created_at) VALUES (?,?,?,?)", 
                    (email, hashed_pw, name, _now_iso()))

def save_chat_message(conversation_id: str, role: str, content: str) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO chat_messages (conversation_id, role, content, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (conversation_id, role, content, _now_iso()),
        )


def save_generated_script(
    conversation_id: str,
    question: str,
    output_format: str,
    reply: str,
    script: str,
    language: str,
    user_id: int = 1,
) -> int:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO generated_scripts (
                user_id, conversation_id, question, output_format, reply, script, language, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                conversation_id,
                question,
                output_format,
                reply,
                script,
                language,
                _now_iso(),
            ),
        )
        return int(cursor.lastrowid)


def list_recent_scripts(limit: int = 6) -> list[dict[str, Any]]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, question, output_format, reply, script, language, created_at
            FROM generated_scripts
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [dict(row) for row in rows]


def list_conversation_messages(conversation_id: str, limit: int = 50) -> list[dict[str, Any]]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, conversation_id, role, content, created_at
            FROM chat_messages
            WHERE conversation_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (conversation_id, limit),
        ).fetchall()

    return [dict(row) for row in rows]


def count_rows(table_name: str) -> int:
    with get_connection() as connection:
        row = connection.execute(f"SELECT COUNT(*) AS total FROM {table_name}").fetchone()
    return int(row["total"] if row else 0)


def count_distinct_conversations() -> int:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT COUNT(DISTINCT conversation_id) AS total FROM chat_messages"
        ).fetchone()
    return int(row["total"] if row else 0)

def list_user_scripts(user_id: int) -> list[dict[str, Any]]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, question, output_format, reply, script, language, created_at 
            FROM generated_scripts 
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (user_id,)
        ).fetchall()
    return [dict(row) for row in rows]

def fetch_summary_for_user(user_id: int):
    with get_connection() as conn:
        scripts = conn.execute(
            "SELECT COUNT(*) as total FROM generated_scripts WHERE user_id = ?", 
            (user_id,)
        ).fetchone()["total"]
        
        # Simulação de horas baseada nos scripts do usuário
        return {
            "scripts_generated": scripts,
            "time_saved_hours": round(scripts * 2.4, 1),
            "active_users": 1, # O próprio usuário
            "success_rate": 94 if scripts > 0 else 0
        }