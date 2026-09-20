# Empirical Transition-Cost Estimation

## Separate quantities

```text
kappa(i->j)      = observed cognitive/interaction effort
theta(i->j|s,u) = transition likelihood/confidence
n(i->j)          = observed frequency
```

They are independent. `kappa != 1 - theta`.

## Per-instance observed cost

For each realized transition, persist components rather than only a scalar:

```text
u_t =
  wT * temporal_effort
+ wN * interaction_steps
+ wR * resistance_or_reversal
+ wS * semantic_cognitive_effort
+ wP * prosodic_effort
+ wF * failure_or_backtrack
```

All components are normalized to [0,1]. The weights are versioned and must be learned/validated rather than silently changed.

## Posterior update

```text
kappa_hat(i->j) =
  n_ij/(n_ij + alpha) * mean(u_ij)
  + alpha/(n_ij + alpha) * kappa_prior(i->j)
```

## CCTDb transition instance

Persist:
- state_before;
- intervention / CogTransition;
- state_after;
- text features;
- prosody features and baseline deltas;
- temporal features;
- outcome;
- cost components;
- aggregate observed cost;
- confidence;
- geography/locale/domain/channel;
- evidence refs;
- extractor and skill versions.

## Validation experiments

1. Does theoretical `kappa_0` correlate with observed difficulty?
2. Does learned `kappa_hat` predict held-out difficulty better than `kappa_0`?
3. Does adding prosody improve held-out prediction?
4. Does contextual/geographic `kappa` outperform a universal matrix?
5. Does NBA conditioned on learned `kappa` improve task outcomes against fixed-cost and constant-cost ablations?
