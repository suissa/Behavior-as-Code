# ABO — Abandonment

## Canonical meaning

Quebra abrupta ou prolongada do fluxo interacional.

This state is a temporary, context-relative BehaviorState. It MUST NOT be persisted as a fixed personality label.

## Identification contract

An Agent/LLM identifies `ABO` only from observable evidence. It should combine syntactic-semantic features, interaction context, prior state, current intent, and—when available—prosodic signals normalized to the same user.

Primary cues:
- Ausência após interação ativa
- interrupção sem fechamento
- expiração de sessão
- abandono após etapa crítica.

## Boundary conditions

Silêncio só vira ABO após regra temporal/contextual; não inferir desinteresse imediatamente.

Never classify from one token, emoji, acoustic feature, or latency value alone. When evidence conflicts, lower confidence and emit competing hypotheses.

## Required output

```json
{
  "state_code": "ABO",
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

1. "[sem resposta após etapa ativa]" — candidate `ABO` when context supports the listed cues.
2. "Usuário some depois de solicitar proposta." — candidate `ABO` when context supports the listed cues.
3. "Sessão expira após início de pagamento." — candidate `ABO` when context supports the listed cues.
4. "Interação interrompida sem encerramento." — candidate `ABO` when context supports the listed cues.

## Counterexamples

- A semantically similar phrase with opposite context must not be forced into `ABO`.
- A strong textual cue contradicted by the longitudinal trajectory must reduce confidence.
- A prosodic cue that deviates from population norms but matches the user's own baseline is weak evidence.

## Prosodic support

Prosody may contribute through baseline-relative speaking rate, pause ratio, RMS energy, F0, F0 variability, jitter/shimmer proxies and response latency. These are evidence features, not diagnoses.

## CCTDb persistence

Persist: state hypothesis, confidence, evidence/counter-evidence refs, BehaviorID transition refs, extractor/skill versions, temporal validity and geographic/context bucket.