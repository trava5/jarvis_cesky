"""
Lokální paměť asistenta.

Běžné dlouhodobé fakty a potvrzená rozhodnutí se ukládají odděleně od
krátkodobé provozní konverzace. Veřejné funkce pro práci s fakty zůstávají
kompatibilní s původním JSON rozhraním.
"""

from __future__ import annotations

import json
import re
import sqlite3
import unicodedata
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent
MEMORY_DIR = BASE_DIR / "memory"
MEMORY_FILE = MEMORY_DIR / "memory.json"
DB_FILE = MEMORY_DIR / "jarvis_memory.sqlite3"
ROOT_VALUE_KEY = "__value__"
SHORT_TERM_RETENTION_DAYS = 31


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _connect() -> sqlite3.Connection:
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _init_db(conn: sqlite3.Connection):
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS memory_items (
            category TEXT NOT NULL,
            item_key TEXT NOT NULL,
            value_json TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            PRIMARY KEY (category, item_key)
        );

        CREATE TABLE IF NOT EXISTS memory_meta (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS conversation_turns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_conversation_turns_session
            ON conversation_turns(session_id, id);
        CREATE INDEX IF NOT EXISTS idx_conversation_turns_created
            ON conversation_turns(created_at);

        CREATE TABLE IF NOT EXISTS short_term_conversation_turns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_short_term_turns_session
            ON short_term_conversation_turns(session_id, id);
        CREATE INDEX IF NOT EXISTS idx_short_term_turns_created
            ON short_term_conversation_turns(created_at);

        CREATE TABLE IF NOT EXISTS long_term_decisions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            decision TEXT NOT NULL,
            rationale TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL DEFAULT 'ACCEPTED',
            source TEXT NOT NULL DEFAULT '',
            confirmed_by TEXT NOT NULL DEFAULT '',
            confirmation_text TEXT NOT NULL DEFAULT '',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_long_term_decisions_created
            ON long_term_decisions(created_at);
        """
    )
    _init_fts(conn)
    _migrate_short_term_turns(conn)
    _migrate_json_memory(conn)
    conn.commit()


def _init_fts(conn: sqlite3.Connection):
    try:
        conn.executescript(
            """
            CREATE VIRTUAL TABLE IF NOT EXISTS conversation_turns_fts
            USING fts5(content, content='conversation_turns', content_rowid='id');

            CREATE TRIGGER IF NOT EXISTS conversation_turns_ai
            AFTER INSERT ON conversation_turns BEGIN
                INSERT INTO conversation_turns_fts(rowid, content)
                VALUES (new.id, new.content);
            END;

            CREATE TRIGGER IF NOT EXISTS conversation_turns_ad
            AFTER DELETE ON conversation_turns BEGIN
                INSERT INTO conversation_turns_fts(conversation_turns_fts, rowid, content)
                VALUES ('delete', old.id, old.content);
            END;

            CREATE TRIGGER IF NOT EXISTS conversation_turns_au
            AFTER UPDATE ON conversation_turns BEGIN
                INSERT INTO conversation_turns_fts(conversation_turns_fts, rowid, content)
                VALUES ('delete', old.id, old.content);
                INSERT INTO conversation_turns_fts(rowid, content)
                VALUES (new.id, new.content);
            END;

            CREATE VIRTUAL TABLE IF NOT EXISTS short_term_conversation_turns_fts
            USING fts5(content, content='short_term_conversation_turns', content_rowid='id');

            CREATE TRIGGER IF NOT EXISTS short_term_conversation_turns_ai
            AFTER INSERT ON short_term_conversation_turns BEGIN
                INSERT INTO short_term_conversation_turns_fts(rowid, content)
                VALUES (new.id, new.content);
            END;

            CREATE TRIGGER IF NOT EXISTS short_term_conversation_turns_ad
            AFTER DELETE ON short_term_conversation_turns BEGIN
                INSERT INTO short_term_conversation_turns_fts(short_term_conversation_turns_fts, rowid, content)
                VALUES ('delete', old.id, old.content);
            END;

            CREATE TRIGGER IF NOT EXISTS short_term_conversation_turns_au
            AFTER UPDATE ON short_term_conversation_turns BEGIN
                INSERT INTO short_term_conversation_turns_fts(short_term_conversation_turns_fts, rowid, content)
                VALUES ('delete', old.id, old.content);
                INSERT INTO short_term_conversation_turns_fts(rowid, content)
                VALUES (new.id, new.content);
            END;
            """
        )
    except sqlite3.DatabaseError:
        # Některé buildy SQLite nemusí mít FTS5. Základní ukládání paměti musí
        # fungovat i bez textového indexu.
        pass


def _ensure_db() -> sqlite3.Connection:
    conn = _connect()
    _init_db(conn)
    return conn


@contextmanager
def _database():
    conn = _ensure_db()
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def _json_dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _json_loads(raw: str) -> Any:
    return json.loads(raw)


def _upsert_item(conn: sqlite3.Connection, category: str, key: str, value: Any):
    now = _utc_now()
    conn.execute(
        """
        INSERT INTO memory_items(category, item_key, value_json, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(category, item_key) DO UPDATE SET
            value_json = excluded.value_json,
            updated_at = excluded.updated_at
        """,
        (category, key, _json_dumps(value), now, now),
    )


def _delete_item(conn: sqlite3.Connection, category: str, key: str) -> int:
    cur = conn.execute(
        "DELETE FROM memory_items WHERE category = ? AND item_key = ?",
        (category, key),
    )
    return int(cur.rowcount or 0)


def _migrate_short_term_turns(conn: sqlite3.Connection):
    migrated = conn.execute(
        "SELECT value FROM memory_meta WHERE key = ?",
        ("short_term_turns_migrated",),
    ).fetchone()
    if migrated:
        return

    conn.execute(
        """
        INSERT INTO short_term_conversation_turns(session_id, role, content, metadata_json, created_at)
        SELECT session_id, role, content, metadata_json, created_at
        FROM conversation_turns
        WHERE NOT EXISTS (
            SELECT 1
            FROM short_term_conversation_turns st
            WHERE st.session_id = conversation_turns.session_id
              AND st.role = conversation_turns.role
              AND st.content = conversation_turns.content
              AND st.created_at = conversation_turns.created_at
        )
        """
    )
    conn.execute(
        "INSERT OR REPLACE INTO memory_meta(key, value) VALUES (?, ?)",
        ("short_term_turns_migrated", _utc_now()),
    )


def _migrate_json_memory(conn: sqlite3.Connection):
    migrated = conn.execute(
        "SELECT value FROM memory_meta WHERE key = ?",
        ("json_migrated",),
    ).fetchone()
    if migrated:
        return

    if not MEMORY_FILE.exists():
        conn.execute(
            "INSERT OR REPLACE INTO memory_meta(key, value) VALUES (?, ?)",
            ("json_migrated", _utc_now()),
        )
        return

    try:
        raw_memory = json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
    except Exception:
        raw_memory = None

    if isinstance(raw_memory, dict):
        for category, items in raw_memory.items():
            category = str(category)
            if isinstance(items, dict):
                for key, value in items.items():
                    _upsert_item(conn, category, str(key), value)
            else:
                _upsert_item(conn, category, ROOT_VALUE_KEY, items)

    conn.execute(
        "INSERT OR REPLACE INTO memory_meta(key, value) VALUES (?, ?)",
        ("json_migrated", _utc_now()),
    )


def purge_short_term_memory(days: int = SHORT_TERM_RETENTION_DAYS, conn: sqlite3.Connection | None = None) -> int:
    from datetime import timedelta

    days = max(1, int(days or SHORT_TERM_RETENTION_DAYS))
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat(timespec="seconds")

    if conn is not None:
        cur = conn.execute(
            "DELETE FROM short_term_conversation_turns WHERE created_at < ?",
            (cutoff,),
        )
        return int(cur.rowcount or 0)

    with _database() as db:
        cur = db.execute(
            "DELETE FROM short_term_conversation_turns WHERE created_at < ?",
            (cutoff,),
        )
        return int(cur.rowcount or 0)


def load_memory() -> dict:
    try:
        with _database() as conn:
            rows = conn.execute(
                """
                SELECT category, item_key, value_json
                FROM memory_items
                ORDER BY category, item_key
                """
            ).fetchall()
    except Exception:
        return {}

    memory: dict[str, Any] = {}
    for row in rows:
        category = str(row["category"])
        key = str(row["item_key"])
        try:
            value = _json_loads(str(row["value_json"]))
        except Exception:
            value = str(row["value_json"])

        if key == ROOT_VALUE_KEY:
            memory[category] = value
            continue

        bucket = memory.setdefault(category, {})
        if isinstance(bucket, dict):
            bucket[key] = value
        else:
            memory[category] = {key: value}

    return memory


def update_memory(data: dict):
    if not isinstance(data, dict):
        return

    with _database() as conn:
        for category, items in data.items():
            category = str(category).strip()
            if not category:
                continue

            if isinstance(items, dict):
                for key, value in items.items():
                    key = str(key).strip()
                    if key:
                        _upsert_item(conn, category, key, value)
            else:
                _upsert_item(conn, category, ROOT_VALUE_KEY, items)


def _normalize_text(text: str) -> str:
    text = (text or "").strip().casefold()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return " ".join(text.split())


def _entry_value_text(value) -> str:
    if isinstance(value, dict):
        base = value.get("value")
        if base is not None:
            return str(base)
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def _tokenize_text(text: str) -> list[str]:
    normalized = _normalize_text(text)
    return [token for token in re.split(r"[^a-z0-9]+", normalized) if token]


def _entry_matches(needle: str, category: str, item_key: str, item_value) -> bool:
    haystacks = [
        _normalize_text(category),
        _normalize_text(item_key),
        _normalize_text(_entry_value_text(item_value)),
    ]
    if any(needle in hay for hay in haystacks):
        return True

    tokens = [tok for tok in _tokenize_text(needle) if len(tok) >= 3]
    if not tokens:
        return False

    entry_tokens: list[str] = []
    for hay in haystacks:
        entry_tokens.extend(_tokenize_text(hay))

    matched = 0
    for token in tokens:
        if any(token in entry_token or entry_token in token for entry_token in entry_tokens):
            matched += 1

    if len(tokens) == 1:
        return matched == 1
    return matched >= min(2, len(tokens))


def delete_memory(category: str = "", key: str = "", match_text: str = "") -> str:
    mem = load_memory()
    if not mem:
        return "V paměti není žádný záznam, který by bylo možné odstranit."

    category = (category or "").strip()
    key = (key or "").strip()
    match_text = (match_text or "").strip()

    if category and key:
        with _database() as conn:
            deleted = _delete_item(conn, category, key)
        if deleted:
            return f"Záznam {category}/{key} byl odstraněn z paměti."
        return "Požadovaný záznam se v paměti nepodařilo najít."

    needle = _normalize_text(match_text or key)
    if not needle:
        return "Pro odstranění záznamu je nutné zadat category/key nebo match_text."

    for cat, bucket in list(mem.items()):
        if not isinstance(bucket, dict):
            if _entry_matches(needle, cat, cat, bucket):
                with _database() as conn:
                    _delete_item(conn, cat, ROOT_VALUE_KEY)
                return f"Záznam {cat} byl odstraněn z paměti."
            continue

        for item_key, item_value in list(bucket.items()):
            if _entry_matches(needle, cat, item_key, item_value):
                with _database() as conn:
                    _delete_item(conn, cat, item_key)
                return f"Záznam {cat}/{item_key} byl odstraněn z paměti."

    return "Odpovídající záznam se v paměti nepodařilo najít."


def save_conversation_turn(
    role: str,
    content: str,
    session_id: str,
    metadata: dict | None = None,
) -> int | None:
    role = str(role or "").strip()
    content = str(content or "").strip()
    session_id = str(session_id or "").strip()

    if not role or not content or not session_id:
        return None

    metadata_json = _json_dumps(metadata or {})
    with _database() as conn:
        purge_short_term_memory(conn=conn)
        cur = conn.execute(
            """
            INSERT INTO short_term_conversation_turns(session_id, role, content, metadata_json, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (session_id, role, content, metadata_json, _utc_now()),
        )
        return int(cur.lastrowid)


def recent_conversation_turns(limit: int = 20, session_id: str = "") -> list[dict]:
    limit = max(1, min(200, int(limit or 20)))
    params: list[Any] = []
    where = ""
    if session_id:
        where = "WHERE session_id = ?"
        params.append(session_id)
    params.append(limit)

    with _database() as conn:
        rows = conn.execute(
            f"""
            SELECT id, session_id, role, content, metadata_json, created_at
            FROM short_term_conversation_turns
            {where}
            ORDER BY id DESC
            LIMIT ?
            """,
            params,
        ).fetchall()

    turns = []
    for row in reversed(rows):
        try:
            metadata = _json_loads(str(row["metadata_json"]))
        except Exception:
            metadata = {}
        turns.append(
            {
                "id": row["id"],
                "session_id": row["session_id"],
                "role": row["role"],
                "content": row["content"],
                "metadata": metadata,
                "created_at": row["created_at"],
            }
        )
    return turns


def search_conversation_text(query: str, limit: int = 10) -> list[dict]:
    query = str(query or "").strip()
    if not query:
        return []
    limit = max(1, min(50, int(limit or 10)))

    with _database() as conn:
        try:
            rows = conn.execute(
                """
                SELECT t.id, t.session_id, t.role, t.content, t.metadata_json, t.created_at
                FROM short_term_conversation_turns_fts f
                JOIN short_term_conversation_turns t ON t.id = f.rowid
                WHERE short_term_conversation_turns_fts MATCH ?
                ORDER BY rank
                LIMIT ?
                """,
                (query, limit),
            ).fetchall()
        except sqlite3.DatabaseError:
            rows = conn.execute(
                """
                SELECT id, session_id, role, content, metadata_json, created_at
                FROM short_term_conversation_turns
                WHERE content LIKE ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (f"%{query}%", limit),
            ).fetchall()

    results = []
    for row in rows:
        try:
            metadata = _json_loads(str(row["metadata_json"]))
        except Exception:
            metadata = {}
        results.append(
            {
                "id": row["id"],
                "session_id": row["session_id"],
                "role": row["role"],
                "content": row["content"],
                "metadata": metadata,
                "created_at": row["created_at"],
            }
        )
    return results


def save_long_term_decision(
    title: str,
    decision: str,
    rationale: str = "",
    source: str = "",
    confirmed: bool = False,
    confirmed_by: str = "user",
    confirmation_text: str = "",
    metadata: dict | None = None,
) -> str:
    title = str(title or "").strip()
    decision = str(decision or "").strip()
    rationale = str(rationale or "").strip()
    source = str(source or "").strip()
    confirmed_by = str(confirmed_by or "").strip()
    confirmation_text = str(confirmation_text or "").strip()

    if not confirmed:
        return "Rozhodnutí nebylo uloženo. Chybí výslovné potvrzení uživatele."
    if not title or not decision:
        return "Rozhodnutí nebylo uloženo. Chybí název nebo text rozhodnutí."
    if not confirmation_text:
        return "Rozhodnutí nebylo uloženo. Chybí text potvrzení uživatele."

    with _database() as conn:
        cur = conn.execute(
            """
            INSERT INTO long_term_decisions(
                title,
                decision,
                rationale,
                status,
                source,
                confirmed_by,
                confirmation_text,
                metadata_json,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                title,
                decision,
                rationale,
                "ACCEPTED",
                source,
                confirmed_by or "user",
                confirmation_text,
                _json_dumps(metadata or {}),
                _utc_now(),
            ),
        )
        decision_id = int(cur.lastrowid)
    return f"Dlouhodobé rozhodnutí LD-{decision_id:04d} bylo uloženo."


def load_long_term_decisions(limit: int = 50) -> list[dict]:
    limit = max(1, min(200, int(limit or 50)))
    with _database() as conn:
        rows = conn.execute(
            """
            SELECT id, title, decision, rationale, status, source,
                   confirmed_by, confirmation_text, metadata_json, created_at
            FROM long_term_decisions
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    decisions = []
    for row in reversed(rows):
        try:
            metadata = _json_loads(str(row["metadata_json"]))
        except Exception:
            metadata = {}
        decisions.append(
            {
                "id": row["id"],
                "title": row["title"],
                "decision": row["decision"],
                "rationale": row["rationale"],
                "status": row["status"],
                "source": row["source"],
                "confirmed_by": row["confirmed_by"],
                "confirmation_text": row["confirmation_text"],
                "metadata": metadata,
                "created_at": row["created_at"],
            }
        )
    return decisions


def format_long_term_decisions_for_prompt(decisions: list[dict] | None = None) -> str:
    decisions = decisions if decisions is not None else load_long_term_decisions()
    if not decisions:
        return ""

    lines = ["[DLOUHODOBÁ PAMĚŤ — POTVRZENÁ ROZHODNUTÍ]"]
    for item in decisions:
        decision_id = int(item.get("id") or 0)
        title = str(item.get("title") or "").strip()
        decision = str(item.get("decision") or "").strip()
        rationale = str(item.get("rationale") or "").strip()
        prefix = f"  LD-{decision_id:04d}"
        if title:
            prefix += f" — {title}"
        lines.append(f"{prefix}: {decision}")
        if rationale:
            lines.append(f"    Důvod: {rationale}")
    return "\n".join(lines)


def format_memory_for_prompt(memory: dict) -> str:
    if not memory:
        return ""
    lines = ["[INFORMACE O UŽIVATELI]"]
    for category, items in memory.items():
        if isinstance(items, dict):
            for key, val in items.items():
                if category == "whatsapp_contacts" and isinstance(val, dict):
                    display_name = val.get("display_name", key)
                    value = val.get("value", "")
                    aliases = val.get("aliases", [])
                    alias_str = ""
                    if isinstance(aliases, list) and aliases:
                        alias_str = f" alternativní_názvy={', '.join(str(a) for a in aliases)}"
                    lines.append(f"  {category}/{display_name}: {value}{alias_str}")
                else:
                    value = val.get("value", val) if isinstance(val, dict) else val
                    lines.append(f"  {category}/{key}: {value}")
        else:
            lines.append(f"  {category}: {items}")
    return "\n".join(lines)
