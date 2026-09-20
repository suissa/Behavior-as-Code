# RES — Resistance

## Canonical meaning

Reatância ou oposição à tentativa de influência, frequentemente com preservação de autonomia.

This state is a temporary, context-relative BehaviorState. It MUST NOT be persisted as a fixed personality label.

## Identification contract

An Agent/LLM identifies `RES` only from observable evidence. It should combine syntactic-semantic features, interaction context, prior state, current intent, and—when available—prosodic signals normalized to the same user.

Primary cues:
- Recusa de pressão
- contestação
- defesa de posição
- irritação com insistência
- linguagem de autonomia.

## Boundary conditions

Não tratar discordância factual simples como resistência; exigir evidência contextual de oposição ao direcionamento.

Never classify from one token, emoji, acoustic feature, or latency value alone. When evidence conflicts, lower confidence and emit competing hypotheses.

## Required output

```json
{
  "state_code": "RES",
  "confidence": 0.0,
  "supporting_evidence": [],
  "contradicting_evidence": [],
  "source_modalities": ["text"],
  "baseline_relative_signals": {},
  "context": {
    "intent": null,
    "topic": null,
    "locale": null,
    "geo_bucket": null
  }
}
```

## Positive examples

1. "Não tenta me empurrar isso." — candidate `RES` when context supports the listed cues.
2. "Eu já disse que não quero esse plano." — candidate `RES` when context supports the listed cues.
3. "Parece que você está insistindo demais." — candidate `RES` when context supports the listed cues.
4. "Prefiro decidir sozinho." — candidate `RES` when context supports the listed cues.

## Counterexamples

- A semantically similar phrase with opposite context must not be forced into `RES`.
- A strong textual cue contradicted by the longitudinal trajectory must reduce confidence.
- A prosodic cue that deviates from population norms but matches the user's own baseline is weak evidence.

## Prosodic support

Prosody may contribute through baseline-relative speaking rate, pause ratio, RMS energy, F0, F0 variability, jitter/shimmer proxies and response latency. These are evidence features, not diagnoses.

## CCTDb persistence

Persist: state hypothesis, confidence, evidence/counter-evidence refs, BehaviorID transition refs, extractor/skill versions, temporal validity and geographic/context bucket.