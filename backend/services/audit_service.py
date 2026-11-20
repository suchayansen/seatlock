
import hashlib
import json

from psycopg import sql


def get_shard_id(event_id=None, actor_id=None):
    """
    Event actions: event_id hash mod 4.
    Non-event actions: actor_id hash mod 4.
    Uses SHA-256 for deterministic routing.
    """

    value = event_id if event_id is not None else actor_id

    if value is None:
        raise ValueError("event_id or actor_id is required")

    digest = hashlib.sha256(str(value).encode()).digest()

    return int.from_bytes(digest[:8], "big") % 4


def write_audit(
    conn,
    action,
    actor_id=None,
    event_id=None,
    entity_type=None,
    entity_id=None,
    details=None
):
    """
    Write an audit record using an existing database transaction.
    """

    shard_id = get_shard_id(event_id, actor_id)
    table_name = f"audit_logs_{shard_id}"

    query = sql.SQL("""
        INSERT INTO {} (
            event_id,
            actor_id,
            action,
            entity_type,
            entity_id,
            details
        )
        VALUES (%s, %s, %s, %s, %s, %s::jsonb)
        RETURNING id, created_at
    """).format(sql.Identifier(table_name))

    result = conn.execute(
        query,
        (
            event_id,
            actor_id,
            action,
            entity_type,
            entity_id,
            json.dumps(details or {})
        )
    ).fetchone()

    return {
        "shard": table_name,
        "id": result[0],
        "created_at": result[1]
    }


def get_audit_logs(conn, event_id=None, actor_id=None, limit=100):
    """Retrieve audit records from the four shards."""

    if event_id is None and actor_id is None:
        raise ValueError("Provide event_id or actor_id")

    if not 1 <= limit <= 500:
        raise ValueError("Limit must be between 1 and 500")

    conditions = []
    params = []

    if event_id is not None:
        conditions.append("event_id = %s")
        params.append(event_id)

    if actor_id is not None:
        conditions.append("actor_id = %s")
        params.append(actor_id)

    where_clause = " AND ".join(conditions)

    query = sql.SQL(" UNION ALL ").join([
        sql.SQL("""
            SELECT id, event_id, actor_id, action,
                   entity_type, entity_id, details, created_at
            FROM {}
            WHERE {}
        """).format(
            sql.Identifier(f"audit_logs_{i}"),
            sql.SQL(where_clause)
        )
        for i in range(4)
    ])

    final_query = sql.SQL("""
        SELECT * FROM ({}) AS audit_results
        ORDER BY created_at DESC
        LIMIT %s
    """).format(query)

    rows = conn.execute(final_query, params * 4 + [limit]).fetchall()

    return [
        {
            "id": row[0],
            "event_id": str(row[1]) if row[1] else None,
            "actor_id": str(row[2]) if row[2] else None,
            "action": row[3],
            "entity_type": row[4],
            "entity_id": str(row[5]) if row[5] else None,
            "details": row[6],
            "created_at": row[7].isoformat()
        }
        for row in rows
    ]
