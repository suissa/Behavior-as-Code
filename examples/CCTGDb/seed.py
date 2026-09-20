#!/usr/bin/env python3
"""Seed a CCTGDb Cozo database with deterministic semantics and UUIDv7 identities."""

from __future__ import annotations

import argparse
import json
import secrets
import threading
import time
import uuid
from pathlib import Path

from pycozo.client import Client


SEMANTIC_DIM = 384
AFFECT_DIM = 16


class UUID7Generator:
    """RFC 9562 UUIDv7 generator with monotonic rand_a inside one millisecond.

    rand_a is a 12-bit monotonic sequence. rand_b keeps 62 bits of CSPRNG
    entropy for every generated identifier.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._last_ms = -1
        self._rand_a = 0

    def __call__(self) -> uuid.UUID:
        with self._lock:
            ms = time.time_ns() // 1_000_000
            if ms != self._last_ms:
                self._last_ms = ms
                self._rand_a = secrets.randbits(12)
            else:
                self._rand_a = (self._rand_a + 1) & 0xFFF
                if self._rand_a == 0:
                    while (time.time_ns() // 1_000_000) <= ms:
                        time.sleep(0)
                    return self()

            rand_b = secrets.randbits(62)
            value = (
                (ms & ((1 << 48) - 1)) << 80
                | 0x7 << 76
                | (self._rand_a & 0xFFF) << 64
                | 0b10 << 62
                | rand_b
            )
            return uuid.UUID(int=value)


uuid7 = UUID7Generator()


def one_hot(dim: int, pos: int, magnitude: float = 1.0) -> list[float]:
    out = [0.0] * dim
    out[pos % dim] = magnitude
    return out


def put_user(db: Client, ids: dict[str, str]) -> None:
    db.run(
        """
        ?[user_id, geo_bucket, locale, current_snapshot_id] :=
            user_id = to_uuid($user_id),
            geo_bucket = $geo_bucket,
            locale = $locale,
            current_snapshot_id = to_uuid($snapshot_id)
        :put user {user_id => geo_bucket, locale, current_snapshot_id}
        """,
        {
            "user_id": ids["user_id"],
            "snapshot_id": ids["snapshot_id"],
            "geo_bucket": "BR/SP/Itarare",
            "locale": "pt-BR",
        },
    )


def put_topic(
    db: Client,
    topic_id: str,
    label: str,
    vector: list[float],
    parent_topic_id: str | None = None,
) -> None:
    if parent_topic_id is None:
        db.run(
            """
            ?[topic_id, canonical_label, semantic_vector, parent_topic_id] :=
                topic_id = to_uuid($topic_id),
                canonical_label = $label,
                semantic_vector = vec($vector),
                parent_topic_id = null
            :put topic {topic_id => canonical_label, semantic_vector, parent_topic_id}
            """,
            {"topic_id": topic_id, "label": label, "vector": vector},
        )
    else:
        db.run(
            """
            ?[topic_id, canonical_label, semantic_vector, parent_topic_id] :=
                topic_id = to_uuid($topic_id),
                canonical_label = $label,
                semantic_vector = vec($vector),
                parent_topic_id = to_uuid($parent_topic_id)
            :put topic {topic_id => canonical_label, semantic_vector, parent_topic_id}
            """,
            {
                "topic_id": topic_id,
                "label": label,
                "vector": vector,
                "parent_topic_id": parent_topic_id,
            },
        )


def put_behavior_state(
    db: Client,
    user_id: str,
    topic_id: str,
    validity: str,
    state_code: str,
    confidence: float,
) -> None:
    db.run(
        """
        ?[user_id, topic_id, validity, state_code, confidence] :=
            user_id = to_uuid($user_id),
            topic_id = to_uuid($topic_id),
            validity = $validity,
            state_code = $state_code,
            confidence = $confidence
        :put behavior_state {
            user_id, topic_id, validity => state_code, confidence
        }
        """,
        {
            "user_id": user_id,
            "topic_id": topic_id,
            "validity": validity,
            "state_code": state_code,
            "confidence": confidence,
        },
    )


def put_transition(
    db: Client,
    *,
    user_id: str,
    topic_id: str,
    transition_id: str,
    validity: str,
    from_state: str,
    to_state: str,
    kappa: float,
    theta: float,
    n: int,
    context: dict,
) -> None:
    db.run(
        """
        ?[user_id, topic_id, transition_id, validity,
          from_state, to_state, kappa, theta, n, context_json] :=
            user_id = to_uuid($user_id),
            topic_id = to_uuid($topic_id),
            transition_id = to_uuid($transition_id),
            validity = $validity,
            from_state = $from_state,
            to_state = $to_state,
            kappa = $kappa,
            theta = $theta,
            n = $n,
            context_json = json($context)
        :put transition {
            user_id, topic_id, transition_id, validity
            =>
            from_state, to_state, kappa, theta, n, context_json
        }
        """,
        {
            "user_id": user_id,
            "topic_id": topic_id,
            "transition_id": transition_id,
            "validity": validity,
            "from_state": from_state,
            "to_state": to_state,
            "kappa": kappa,
            "theta": theta,
            "n": n,
            "context": context,
        },
    )


def put_message(
    db: Client,
    *,
    message_id: str,
    user_id: str,
    topic_id: str,
    semantic: list[float],
    affect: list[float],
    timestamp_us: int,
) -> None:
    db.run(
        """
        ?[message_id, user_id, topic_id, semantic_vector, affect_vector, timestamp] :=
            message_id = to_uuid($message_id),
            user_id = to_uuid($user_id),
            topic_id = to_uuid($topic_id),
            semantic_vector = vec($semantic),
            affect_vector = vec($affect),
            timestamp = $timestamp
        :put message_semantic {
            message_id
            =>
            user_id, topic_id, semantic_vector, affect_vector, timestamp
        }
        """,
        {
            "message_id": message_id,
            "user_id": user_id,
            "topic_id": topic_id,
            "semantic": semantic,
            "affect": affect,
            "timestamp": timestamp_us,
        },
    )


def seed(db: Client) -> dict[str, str]:
    ids = {
        "user_id": str(uuid7()),
        "snapshot_id": str(uuid7()),
        "commerce_topic_id": str(uuid7()),
        "pricing_topic_id": str(uuid7()),
        "delivery_topic_id": str(uuid7()),
        "transition_id": str(uuid7()),
        "message_1_id": str(uuid7()),
        "message_2_id": str(uuid7()),
        "message_3_id": str(uuid7()),
    }

    put_user(db, ids)

    put_topic(
        db,
        ids["commerce_topic_id"],
        "Commerce",
        one_hot(SEMANTIC_DIM, 0),
    )
    put_topic(
        db,
        ids["pricing_topic_id"],
        "Commerce.Pricing",
        one_hot(SEMANTIC_DIM, 1),
        ids["commerce_topic_id"],
    )
    put_topic(
        db,
        ids["delivery_topic_id"],
        "Commerce.Delivery",
        one_hot(SEMANTIC_DIM, 2),
        ids["commerce_topic_id"],
    )

    # Same (user, topic), three historical assertions.
    put_behavior_state(
        db,
        ids["user_id"],
        ids["pricing_topic_id"],
        "2026-09-20T12:00:00Z",
        "HES",
        0.78,
    )
    put_behavior_state(
        db,
        ids["user_id"],
        ids["pricing_topic_id"],
        "2026-09-20T12:05:00Z",
        "COM",
        0.89,
    )
    put_behavior_state(
        db,
        ids["user_id"],
        ids["pricing_topic_id"],
        "2026-09-20T12:10:00Z",
        "ACE",
        0.91,
    )

    put_transition(
        db,
        user_id=ids["user_id"],
        topic_id=ids["pricing_topic_id"],
        transition_id=ids["transition_id"],
        validity="2026-09-20T12:05:00Z",
        from_state="HES",
        to_state="COM",
        kappa=0.37,
        theta=0.71,
        n=28,
        context={
            "domain": "sales",
            "locale": "pt-BR",
            "geo_bucket": "BR/SP/Itarare",
            "channel": "audio",
            "situation": "pricing_evaluation",
        },
    )

    base_ts = 1_758_369_600_000_000
    put_message(
        db,
        message_id=ids["message_1_id"],
        user_id=ids["user_id"],
        topic_id=ids["pricing_topic_id"],
        semantic=one_hot(SEMANTIC_DIM, 1, 0.95),
        affect=one_hot(AFFECT_DIM, 2, 0.65),
        timestamp_us=base_ts,
    )
    put_message(
        db,
        message_id=ids["message_2_id"],
        user_id=ids["user_id"],
        topic_id=ids["pricing_topic_id"],
        semantic=one_hot(SEMANTIC_DIM, 1, 0.90),
        affect=one_hot(AFFECT_DIM, 4, 0.72),
        timestamp_us=base_ts + 300_000_000,
    )
    put_message(
        db,
        message_id=ids["message_3_id"],
        user_id=ids["user_id"],
        topic_id=ids["delivery_topic_id"],
        semantic=one_hot(SEMANTIC_DIM, 2, 0.93),
        affect=one_hot(AFFECT_DIM, 7, 0.80),
        timestamp_us=base_ts + 600_000_000,
    )

    return ids


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default="examples/CCTGDb/cctgdb.sqlite")
    parser.add_argument(
        "--schema",
        default=str(Path(__file__).with_name("schema.cozo")),
    )
    args = parser.parse_args()

    db = Client("sqlite", args.db, dataframe=False)
    try:
        if args.schema:
            schema = Path(args.schema).read_text(encoding="utf-8")
            db.run(schema)
        ids = seed(db)
        print(json.dumps(ids, indent=2, sort_keys=True))
    finally:
        db.close()


if __name__ == "__main__":
    main()
