# AAN — Anxiety

## Canonical meaning

Estado situacional de apreensão/urgência percebida, tratado apenas como hipótese comportamental temporária.

This state is a temporary, context-relative BehaviorState. It MUST NOT be persisted as a fixed personality label.

## Identification contract

An Agent/LLM identifies `AAN` only from observable evidence. It should combine syntactic-semantic features, interaction context, prior state, current intent, and—when available—prosodic signals normalized to the same user.

Primary cues:
- Urgência combinada com incerteza
- preocupação
- repetição
- prosódia de alta ativação relativa ao baseline.

## Boundary conditions

Nunca diagnosticar transtorno; não mapear voz rápida ou urgência isolada diretamente para AAN.

Never classify from one token, emoji, acoustic feature, or latency value alone. When evidence conflicts, lower confidence and emit competing hypotheses.

## Required output

```json
{
  "state_code": "AAN",
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

1. "Preciso resolver isso agora, estou preocupado." — candidate `AAN` when context supports the listed cues.
2. "E se der errado? Preciso de uma resposta hoje." — candidate `AAN` when context supports the listed cues.
3. "Não estou tranquilo com isso." — candidate `AAN` when context supports the listed cues.
4. "Me ajuda, isso está me deixando muito tenso." — candidate `AAN` when context supports the listed cues.

## Counterexamples

- A semantically similar phrase with opposite context must not be forced into `AAN`.
- A strong textual cue contradicted by the longitudinal trajectory must reduce confidence.
- A prosodic cue that deviates from population norms but matches the user's own baseline is weak evidence.

## Prosodic support

Prosody may contribute through baseline-relative speaking rate, pause ratio, RMS energy, F0, F0 variability, jitter/shimmer proxies and response latency. These are evidence features, not diagnoses.

## CCTDb persistence

Persist: state hypothesis, confidence, evidence/counter-evidence refs, BehaviorID transition refs, extractor/skill versions, temporal validity and geographic/context bucket.