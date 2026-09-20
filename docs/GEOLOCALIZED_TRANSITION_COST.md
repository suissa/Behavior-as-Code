# Geolocalized Transition-Cost Matrix

## Principle

`kappa(i -> j)` is not universal. Behavioral transition difficulty may vary by geography, locale, language, culture, domain, channel and situation.

The canonical estimator is conditional:

```text
kappa(i,j | domain, locale, geo, channel, situation)
```

A global matrix is only a fallback prior or a marginal projection.

## Geographic hierarchy

Use hierarchical buckets, not raw precise location by default:

```text
global
  -> country
    -> region/state
      -> metro/city
```

Only create a finer bucket when sample size and privacy policy permit. Never infer a universal cultural property from sparse local data.

## Posterior hierarchy

For a cell `i -> j`:

```text
kappa_geo =
  n_geo/(n_geo + alpha_geo) * u_geo
  + alpha_geo/(n_geo + alpha_geo) * kappa_parent
```

where the parent may be city->state->country->global->theory prior.

This gives partial pooling: local evidence dominates when abundant; sparse geographies shrink toward broader priors.

## Required keys

```json
{
  "from_state": "HES",
  "to_state": "COM",
  "domain": "sales",
  "language": "pt-BR",
  "country": "BR",
  "region": "SP",
  "locality": "Itarare",
  "channel": "audio",
  "n": 0,
  "mean_observed_cost": 0.0,
  "posterior_kappa": 0.0,
  "ci95": [0.0, 1.0],
  "parent_prior_ref": "",
  "updated_at": ""
}
```

## Invariants

- geographic bucket is context, never identity or personality;
- report sample size and uncertainty with every local estimate;
- low-support cells inherit broader priors;
- compare geographies only after controlling for domain/channel/situation where possible;
- never encode protected-group stereotypes;
- CCTDb stores provenance for each aggregate.
