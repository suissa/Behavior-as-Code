# Expected synthetic interpretation

The fixture is intentionally tiny and MUST NOT be read as empirical evidence.

It only demonstrates the contract.

For `RES -> ACE`:

- the `after-pressure` observation carries higher observed cost;
- the `after-discount` observation carries lower observed cost;
- the `support` example differs from the sales examples;
- context posteriors shrink toward the global posterior because each context has only one observation.

With real data the report may produce a shape such as:

```text
RES -> ACE
global:          0.78
sales:           0.83
support:         0.61
after-discount:  0.52
after-pressure:  0.91
```

but those numbers are examples until supported by observations.

## Graph interpretation

Treat them as edge weights in separate contextual layers:

```text
sales layer:
RES --0.83--> ACE

support layer:
RES --0.61--> ACE

after-discount layer:
RES --0.52--> ACE

after-pressure layer:
RES --0.91--> ACE
```

Distance between states is then derived from path cost.

Node height is also derived, for example:

```text
height(v) = shortest posterior cost from v to ACE
```

This creates a topological surface over BehaviorStates while preserving the rule that the primitive measured quantity is the directed transition edge.

## Not causality

If `RES -> ACE` is cheaper after a discount, this alone does NOT establish that discounts caused acceptance.

It establishes only a context-conditioned association in the observed trajectories. Causal claims require a separate causal design/evidence layer.
