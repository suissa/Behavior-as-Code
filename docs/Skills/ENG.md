# ENG — Engagement

## Canonical meaning

Investimento de tempo e atenção; respostas detalhadas, afirmativas e cooperativas.

This state is a temporary, context-relative BehaviorState. It MUST NOT be persisted as a fixed personality label.

## Identification contract

An Agent/LLM identifies `ENG` only from observable evidence. It should combine syntactic-semantic features, interaction context, prior state, current intent, and—when available—prosodic signals normalized to the same user.

Primary cues:
- Respostas longas
- expansão espontânea de contexto
- continuidade rápida
- aceitação de perguntas de aprofundamento.

## Boundary conditions

Não confundir com ACE: engajamento não implica concordância final; nem com CUR quando predominam perguntas exploratórias.

Never classify from one token, emoji, acoustic feature, or latency value alone. When evidence conflicts, lower confidence and emit competing hypotheses.

## Required output

```json
{
  "state_code": "ENG",
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

1. "Sim, faz sentido. Hoje usamos três canais e o maior problema é conciliar tudo." — candidate `ENG` when context supports the listed cues.
2. "Posso te explicar como fazemos hoje?" — candidate `ENG` when context supports the listed cues.
3. "Entendi, continua." — candidate `ENG` when context supports the listed cues.
4. "Vou te mandar os dados que você pediu." — candidate `ENG` when context supports the listed cues.

## Counterexamples

- A semantically similar phrase with opposite context must not be forced into `ENG`.
- A strong textual cue contradicted by the longitudinal trajectory must reduce confidence.
- A prosodic cue that deviates from population norms but matches the user's own baseline is weak evidence.

## Prosodic support

Prosody may contribute through baseline-relative speaking rate, pause ratio, RMS energy, F0, F0 variability, jitter/shimmer proxies and response latency. These are evidence features, not diagnoses.

## CCTDb persistence

Persist: state hypothesis, confidence, evidence/counter-evidence refs, BehaviorID transition refs, extractor/skill versions, temporal validity and geographic/context bucket.