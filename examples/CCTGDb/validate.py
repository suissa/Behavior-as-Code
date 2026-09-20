#!/usr/bin/env python3
"""Executable CI validation for the CCTGDb example architecture."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from pycozo.client import Client

from seed import seed


HERE = Path(__file__).resolve().parent


def rows(result):
    return result["rows"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default=str(HERE / ".ci-cctgdb.sqlite"))
    args = parser.parse_args()

    db_path = Path(args.db)
    if db_path.exists():
        db_path.unlink()

    db = Client("sqlite", str(db_path), dataframe=False)
    try:
        db.run((HERE / "schema.cozo").read_text(encoding="utf-8"))
        ids = seed(db)

        rels = db.run("::relations")
        relation_names = {r[0] for r in rows(rels)}
        expected = {
            "user",
            "behavior_state",
            "transition",
            "topic",
            "message_semantic",
        }
        missing = expected - relation_names
        assert not missing, f"missing relations: {sorted(missing)}"

        user_count = rows(
            db.run("?[count(user_id)] := *user{user_id}")
        )[0][0]
        assert user_count == 1, user_count

        topic_count = rows(
            db.run("?[count(topic_id)] := *topic{topic_id}")
        )[0][0]
        assert topic_count == 3, topic_count

        message_count = rows(
            db.run("?[count(message_id)] := *message_semantic{message_id}")
        )[0][0]
        assert message_count == 3, message_count

        # Time travel must return the historical state valid at each point.
        q = """
        ?[state_code] :=
            uid = to_uuid($user_id),
            tid = to_uuid($topic_id),
            *behavior_state{
                user_id: uid,
                topic_id: tid,
                state_code,
                @ '2026-09-20T12:07:00Z'
            }
        """
        historical = rows(
            db.run(
                q,
                {
                    "user_id": ids["user_id"],
                    "topic_id": ids["pricing_topic_id"],
                },
            )
        )
        assert historical == [["COM"]], historical

        current = rows(
            db.run(
                """
                ?[state_code] :=
                    uid = to_uuid($user_id),
                    tid = to_uuid($topic_id),
                    *behavior_state{
                        user_id: uid,
                        topic_id: tid,
                        state_code,
                        @ 'END'
                    }
                """,
                {
                    "user_id": ids["user_id"],
                    "topic_id": ids["pricing_topic_id"],
                },
            )
        )
        assert current == [["ACE"]], current

        trans = rows(
            db.run(
                """
                ?[kappa, theta, n] :=
                    uid = to_uuid($user_id),
                    *transition{user_id: uid, kappa, theta, n}
                """,
                {"user_id": ids["user_id"]},
            )
        )
        assert len(trans) == 1
        kappa, theta, n = trans[0]
        assert abs(kappa - 0.37) < 1e-9
        assert abs(theta - 0.71) < 1e-9
        assert n == 28

        # HNSW query: pricing topic vector must retrieve a topic.
        vector_query = [0.0] * 384
        vector_query[1] = 1.0
        nearest = rows(
            db.run(
                """
                ?[dist, canonical_label] :=
                    q = vec($q),
                    ~topic:semantic{
                        topic_id |
                        query: q,
                        k: 2,
                        ef: 32,
                        bind_distance: dist,
                    },
                    *topic{topic_id, canonical_label}
                :order dist
                :limit 1
                """,
                {"q": vector_query},
            )
        )
        assert nearest, "HNSW returned no topic"
        assert nearest[0][1] == "Commerce.Pricing", nearest

        print("CCTGDb schema + seed validation: OK")
    finally:
        db.close()
        if db_path.exists():
            os.remove(db_path)


if __name__ == "__main__":
    main()
