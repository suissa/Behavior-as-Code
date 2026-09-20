# CCTDb Behavior Snapshot

CCTDb is the consolidated behavioral memory. CCT-RAG retrieves evidence and may infer candidate cognitive-emotional states.

The snapshot stores signals, transitions, evidence, counter-evidence, individual baselines, situational patterns, intent trajectories, geographic/context buckets and cognitive-emotional hypotheses with confidence.

## Hypothesis boundary

```text
observation != inference
inference != fact
hypothesis != personality
```

Every cognitive-emotional hypothesis must include:
- confidence;
- valid_from / valid_to;
- supporting evidence;
- contradicting evidence;
- signal refs;
- transition refs;
- pattern refs;
- method/model/skill version.

## Audio-first baseline

Maintain per-user distributions for:
- speaking_rate_wpm;
- pause_ratio;
- RMS;
- mean F0;
- F0 variability;
- jitter/shimmer proxies;
- response latency.

A single acoustic feature must never determine a state.

## Compaction safety

Raw messages/events/audio become eligible for archive/deletion only after a durable snapshot preserves source cursors, provenance, uncertainty, evidence/counter-evidence, versioned baselines, extractor/skill versions and all retention/audit obligations.
