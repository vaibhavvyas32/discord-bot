import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "bot.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as connection:

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                message_id INTEGER PRIMARY KEY,
                guild_id INTEGER NOT NULL,
                channel_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                username TEXT NOT NULL,
                content TEXT,
                created_at TEXT,
                deleted_at TIMESTAMP,
                is_deleted INTEGER DEFAULT 0
            )
            """
        )

        connection.commit()


def save_message(
    message_id,
    guild_id,
    channel_id,
    user_id,
    username,
    content,
    created_at
):
    with get_connection() as connection:

        connection.execute(
            """
            INSERT OR REPLACE INTO messages (
                message_id,
                guild_id,
                channel_id,
                user_id,
                username,
                content,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                message_id,
                guild_id,
                channel_id,
                user_id,
                username,
                content,
                created_at
            )
        )

        connection.commit()


def mark_message_deleted(message_id):
    with get_connection() as connection:

        connection.execute(
            """
            UPDATE messages
            SET
                is_deleted = 1,
                deleted_at = CURRENT_TIMESTAMP
            WHERE message_id = ?
            """,
            (message_id,)
        )

        connection.commit()


def get_latest_deleted_message(
    guild_id,
    channel_id
):
    with get_connection() as connection:

        message = connection.execute(
            """
            SELECT *
            FROM messages
            WHERE guild_id = ?
            AND channel_id = ?
            AND is_deleted = 1
            ORDER BY deleted_at DESC
            LIMIT 1
            """,
            (
                guild_id,
                channel_id
            )
        ).fetchone()

    return message