# CCTGDb schemas

Reference schema for the Cognitive-Causal-Temporal-Topological Graph Database (CCTGDb) using CozoDB.

## ID policy: UUIDv7

Every canonical `*_id` is a standards-compliant UUIDv7 stored as Cozo `Uuid`.

Do **not** append a custom entropy suffix. UUIDv7 already combines a millisecond Unix timestamp with random/monotonic fields while preserving the 128-bit UUID representation. A custom suffix would turn the identifier into a proprietary string and lose Cozo's native `Uuid` type.

The runtime generator SHOULD:
- use the UUIDv7 timestamp field;
- use cryptographically secure randomness for the random field;
- use a monotonic `rand_a` sequence for IDs emitted inside the same millisecond;
- never derive randomness from `user_id`, location, message contents or other PII;
- expose IDs only as canonical hyphenated UUID strings at boundaries.

Conceptually:

```text
UUIDv7
┌────────────────┬─────────┬────────────┬─────────┬──────────────────────────┐
│ unix_ts_ms 48b │ ver 4b  │ rand_a 12b │ var 2b  │ rand_b 62b               │
└────────────────┴─────────┴────────────┴─────────┴──────────────────────────┘
```

This gives 74 bits in the UUIDv7 random/monotonic area without extending the identifier.

## Vector dimensions used by this executable example

The example fixes dimensions because Cozo vector columns and HNSW indexes require fixed dimensions:

- `SEMANTIC_VECTOR_DIM = 384`
- `AFFECT_VECTOR_DIM = 16`

These are example defaults, not architectural constants. A production CCTGDbManager must bind them to the selected embedding contracts and migrate/rebuild indexes when the model dimensionality changes.

## 1. user

```text
user {
  user_id: Uuid =>
  geo_bucket: String,
  locale: String,
  current_snapshot_id: Uuid?
}
```

`geo_bucket` is a coarse contextual bucket (for example `BR/SP/Itarare`), not precise location. `current_snapshot_id` is nullable until the first consolidated snapshot is emitted.

## 2. behavior_state

```text
behavior_state {
  user_id: Uuid,
  topic_id: Uuid,
  validity: Validity =>
  state_code: String,
  confidence: Float
}
```

The final key is `Validity`, therefore Cozo time-travel is enabled for each `(user_id, topic_id)` history. The current state is a temporal assertion, never a permanent personality label.

## 3. transition

```text
transition {
  user_id: Uuid,
  topic_id: Uuid,
  transition_id: Uuid,
  validity: Validity =>
  from_state: String,
  to_state: String,
  kappa: Float,
  theta: Float,
  n: Int,
  context_json: Json
}
```

Semantics:

```text
kappa(i->j)      = empirical transition cost
theta(i->j|s,u) = transition probability/confidence under situation/user context
n(i->j)         = observed frequency supporting the estimate
```

`kappa`, `theta` and `n` are independent measurements.

## 4. topic

```text
topic {
  topic_id: Uuid =>
  canonical_label: String,
  semantic_vector: <F32; 384>,
  parent_topic_id: Uuid?
}
```

A canonical topic is a semantic cluster such as `Commerce.Pricing`. The HNSW index maps new messages to candidate canonical topics without making vector similarity a source of truth.

## 5. message_semantic

```text
message_semantic {
  message_id: Uuid =>
  user_id: Uuid,
  topic_id: Uuid,
  semantic_vector: <F32; 384>,
  affect_vector: <F32; 16>,
  timestamp: Int
}
```

`timestamp` is Unix epoch microseconds. Raw text is deliberately absent from this compact semantic relation. Retention/audit policy decides whether the original message is retained elsewhere.

## HNSW indexes

The executable schema creates:

```text
topic:semantic
message_semantic:semantic
message_semantic:affect
```

with cosine distance.

## Executable files

- `schema.cozo`: creates all relations and HNSW indexes.
- `seed.py`: generates UUIDv7 IDs and inserts a small temporal/semantic fixture.
- `validate.py`: creates a fresh SQLite-backed Cozo database, runs the schema and seed, and validates relational, temporal and vector behavior.
- `.github/workflows/cctgdb-schema.yml`: executes the validation in CI.
