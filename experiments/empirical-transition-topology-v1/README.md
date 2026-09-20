# Experiment: Empirical Transition Topology v1

## Research question

Can empirically observed BehaviorID transition costs produce a stable, predictive cognitive-behavioral topology?

The experiment estimates context-conditioned transition cost:

```text
kappa(i -> j | context)
```

and projects those directed edge weights into a graph topology without treating adjacency as causality.

Example:

```text
RES -> ACE

global          0.78
domain:sales    0.83
domain:support  0.61
after:discount  0.52
after:pressure  0.91
```

These values are NOT five positions for ACE. They are five edge-weight observations/estimators for the same directed transition under different contexts.

## Core graph

```text
G_c = (V, E, W_c)
```

where:

- `V` = BehaviorStates;
- `E` = observed directed CogTransitions;
- `W_c(i,j) = kappa_hat(i -> j | c)`;
- `c` = context slice such as domain, situation, locale, channel, cohort or intervention.

The topology is therefore a **contextual directed weighted multiplex graph**.

## Distances

For a fixed context `c`, define behavioral path distance as the minimum accumulated transition cost:

```text
d_c(i,j) = min_path sum(kappa_hat(edge | c))
```

Because transitions are directed:

```text
d_c(i,j) != d_c(j,i)
```

in general.

This gives a behavioral geodesic over the graph.

### Example

If:

```text
RES -> HES = 0.20
HES -> ACE = 0.30
RES -> ACE = 0.83
```

then:

```text
d(RES, ACE) = 0.50
```

through `RES -> HES -> ACE`, even though the direct edge costs `0.83`.

This is useful for Next Best Action: choose a feasible low-cost path, not merely the cheapest immediate edge.

## Height / potential

Do not use raw `kappa(i,j)` as node height because `kappa` belongs to an edge.

A node height may be derived from an anchor state `a`:

```text
h_c(v | a) = d_c(a, v)
```

or from a task-specific potential:

```text
h_c(v) = expected_remaining_cost(v -> target)
```

Examples:

- distance from `CUR`;
- distance to `ACE`;
- expected cost to task completion;
- expected cost to safe/regulated state.

Height is therefore a projection of graph structure, not a primitive BehaviorState property.

## Multiplex contexts

Each context forms a layer:

```text
Layer: global
Layer: domain=sales
Layer: domain=support
Layer: situation=after-discount
Layer: situation=after-pressure
Layer: locale=pt-BR
Layer: channel=audio
...
```

The same edge may have different posterior costs per layer.

Sparse layers use hierarchical partial pooling toward parent layers:

```text
specific context
  -> domain/locale parent
  -> global empirical
  -> theoretical prior kappa_0
```

## Observation unit

Every realized BehaviorID transition produces a TransitionObservation:

```text
[b_(t-1)] --tau_t--> [b_t]
```

with:

- source state;
- target state;
- intervention/transition label;
- context dimensions;
- temporal effort;
- interaction-step effort;
- resistance/reversal;
- semantic effort;
- prosodic effort;
- failure/backtrack;
- outcome;
- confidence;
- evidence and counter-evidence refs;
- extractor/skill versions.

The aggregate observed cost is:

```text
u_t =
  wT * temporal_effort
+ wN * interaction_steps
+ wR * resistance_or_reversal
+ wS * semantic_cognitive_effort
+ wP * prosodic_effort
+ wF * failure_or_backtrack
```

Weights are versioned and estimated/validated independently.

## Posterior edge weight

For edge `i -> j` in context `c`:

```text
kappa_hat(i->j | c) =
  n/(n + alpha) * mean(u | i,j,c)
  + alpha/(n + alpha) * kappa_parent(i->j | parent(c))
```

At the global layer, `kappa_parent = kappa_0`.

Persist both:

- `kappa_prior`;
- `kappa_empirical_mean`;
- `kappa_posterior`;
- sample count;
- variance/stddev;
- confidence interval;
- effective context.

## Independent quantities

Do not conflate:

```text
kappa(i->j|c) = transition effort/cost
theta(i->j|c) = likelihood/confidence of transition
n(i->j|c)     = observation count
```

`kappa != 1 - theta`.

## Experimental phases

### E1 — Measurement validity

Test whether the component-based `u_t` is internally consistent and whether different extractors/annotators agree on the observable components.

Outputs:
- component distributions;
- missingness;
- inter-rater/extractor agreement where available;
- calibration by confidence bucket.

### E2 — Prior vs empirical cost

Hypothesis H1:

```text
corr(kappa_0, observed difficulty) > 0
```

Compare the theory prior with held-out observed costs.

### E3 — Posterior prediction

Hypothesis H2:

```text
kappa_hat predicts held-out transition difficulty
better than kappa_0 and constant-cost baselines.
```

Baselines:
- theoretical prior;
- constant cost;
- empirical global mean;
- context-free posterior;
- context-conditioned posterior.

### E4 — Multimodal ablation

Hypothesis H3:

Prosody improves prediction for ambiguous cases without degrading calibrated performance when audio is noisy.

Compare:
- text only;
- text + temporal;
- text + prosody;
- text + temporal + prosody.

### E5 — Topological utility

Hypothesis H4:

Shortest-cost path over the learned graph predicts successful/efficient trajectories better than direct-edge greedy selection.

Compare:
- direct cheapest next edge;
- shortest cumulative path;
- unweighted hop count;
- random valid path.

### E6 — Context topology

Hypothesis H5:

Contextual layers are measurably different where sufficient data exists.

For each edge/context:
- delta from global;
- uncertainty interval;
- sample count;
- shrinkage amount.

No contextual layer is published as different unless its uncertainty supports that distinction.

### E7 — Next Best Action

Hypothesis H6:

NBA conditioned on the learned topology improves a predeclared task outcome over:
- no BehaviorID;
- fixed prior matrix;
- global empirical matrix;
- constant matrix.

## Train/validation/test split

Split by conversation/session, never by individual transition row, to avoid leakage from adjacent transitions.

Where user-level longitudinal data is used, optionally add a stricter subject-held-out evaluation.

## Primary metrics

Cost prediction:
- MAE;
- RMSE;
- rank correlation;
- calibration by predicted-cost bucket.

Topology/path:
- path-cost prediction error;
- successful-path ranking;
- trajectory completion rate;
- excess cost above best observed path.

Context:
- posterior delta from global;
- uncertainty interval width;
- effective sample size;
- shrinkage ratio.

## Topology stability

A learned topology is considered stable only if:

1. high-support edge weights remain similar across resamples;
2. shortest paths are not dominated by single low-support edges;
3. contextual differences survive held-out evaluation;
4. small perturbations do not radically reorder the graph without corresponding uncertainty;
5. edge directionality is preserved.

## Scientific invariants

1. Topological adjacency is not causal evidence.
2. A short path does not mean an intervention causes the destination state.
3. BehaviorState is situational, not a personality label.
4. Context-conditioned costs require uncertainty and sample size.
5. Prosody is evidence, not diagnosis.
6. Raw context may influence weights, but protected/sensitive attributes must not silently become optimization targets.
7. Every published edge weight must be reproducible from versioned observations and configuration.

## Artifacts

This experiment directory contains:

- `config.yml`: versioned experimental parameters;
- `transition-observation.schema.json`: canonical observation contract;
- `fixtures/res-ace.example.ndjson`: synthetic example records;
- `src/analyze.py`: reference posterior/topology analyzer;
- `EXPECTED_OUTPUT.md`: expected synthetic example interpretation.

## Publication criterion

The transition-cost claim is ready for stronger empirical wording only after:

- enough observations exist for predeclared high-value transitions;
- posterior costs beat or calibrate better than the fixed prior on held-out data;
- ablations show which modalities contribute;
- graph topology is stable under resampling;
- all costs retain provenance and uncertainty.
