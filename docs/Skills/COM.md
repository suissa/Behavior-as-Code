# COM — Comparison

## Canonical meaning

Avaliação de custo de oportunidade e contraste entre alternativas.

This state is a temporary, context-relative BehaviorState. It MUST NOT be persisted as a fixed personality label.

## Identification contract

An Agent/LLM identifies `COM` only from observable evidence. It should combine syntactic-semantic features, interaction context, prior state, current intent, and—when available—prosodic signals normalized to the same user.

Primary cues:
- Comparativos explícitos
- critérios
- preço versus benefício
- 'melhor/pior'
- concorrentes
- trade-offs.

## Boundary conditions

Não confundir com CUR: COM pressupõe alternativas ou critérios em comparação.

Never classify from one token, emoji, acoustic feature, or latency value alone. When evidence conflicts, lower confidence and emit competing hypotheses.

## Required output

```json
{
  "state_code": "COM",
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

1. "Esse é mais barato, mas o seu inclui suporte?" — candidate `COM` when context supports the listed cues.
2. "Qual a diferença entre o plano A e o B?" — candidate `COM` when context supports the listed cues.
3. "Na empresa X custa menos." — candidate `COM` when context supports the listed cues.
4. "Entre prazo e preço, qual compensa mais?" — candidate `COM` when context supports the listed cues.

## Counterexamples

- A semantically similar phrase with opposite context must not be forced into `COM`.
- A strong textual cue contradicted by the longitudinal trajectory must reduce confidence.
- A prosodic cue that deviates from population norms but matches the user's own baseline is weak evidence.

## Prosodic support

Prosody may contribute through baseline-relative speaking rate, pause ratio, RMS energy, F0, F0 variability, jitter/shimmer proxies and response latency. These are evidence features, not diagnoses.

## CCTDb persistence

Persist: state hypothesis, confidence, evidence/counter-evidence refs, BehaviorID transition refs, extractor/skill versions, temporal validity and geographic/context bucket.