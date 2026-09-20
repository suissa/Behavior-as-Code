# VAL — Validation

## Canonical meaning

Busca de confirmação, segurança ou prova social antes de avançar.

This state is a temporary, context-relative BehaviorState. It MUST NOT be persisted as a fixed personality label.

## Identification contract

An Agent/LLM identifies `VAL` only from observable evidence. It should combine syntactic-semantic features, interaction context, prior state, current intent, and—when available—prosodic signals normalized to the same user.

Primary cues:
- Pedidos de opinião
- confirmação repetida
- referências a outros usuários/casos
- necessidade de garantia externa.

## Boundary conditions

Não confundir com HES: VAL é especificamente busca de validação externa/social.

Never classify from one token, emoji, acoustic feature, or latency value alone. When evidence conflicts, lower confidence and emit competing hypotheses.

## Required output

```json
{
  "state_code": "VAL",
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

1. "Você acha que estou fazendo a escolha certa?" — candidate `VAL` when context supports the listed cues.
2. "Outras empresas usam isso?" — candidate `VAL` when context supports the listed cues.
3. "Tem algum caso parecido com o meu?" — candidate `VAL` when context supports the listed cues.
4. "Você confirma que esse é o melhor para esse cenário?" — candidate `VAL` when context supports the listed cues.

## Counterexamples

- A semantically similar phrase with opposite context must not be forced into `VAL`.
- A strong textual cue contradicted by the longitudinal trajectory must reduce confidence.
- A prosodic cue that deviates from population norms but matches the user's own baseline is weak evidence.

## Prosodic support

Prosody may contribute through baseline-relative speaking rate, pause ratio, RMS energy, F0, F0 variability, jitter/shimmer proxies and response latency. These are evidence features, not diagnoses.

## CCTDb persistence

Persist: state hypothesis, confidence, evidence/counter-evidence refs, BehaviorID transition refs, extractor/skill versions, temporal validity and geographic/context bucket.