#!/usr/bin/env python3
"""Reference analyzer for Behavior-as-Code empirical transition topology.

Uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import heapq
import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import mean, pstdev

DEFAULT_PRIOR = 0.78


def load_ndjson(path: Path):
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def context_keys(row):
    c = row.get("context", {})
    keys = ["global"]
    for dimension in ("domain", "situation", "locale", "channel"):
        value = c.get(dimension)
        if value:
            keys.append(f"{dimension}:{value}")
    return keys


def posterior(values, prior, alpha):
    if not values:
        return prior
    n = len(values)
    empirical = mean(values)
    return (n / (n + alpha)) * empirical + (alpha / (n + alpha)) * prior


def ci95(values):
    if len(values) < 2:
        return None
    mu = mean(values)
    sd = pstdev(values)
    half = 1.96 * sd / math.sqrt(len(values))
    return [max(0.0, mu - half), min(1.0, mu + half)]


def aggregate(rows, alpha=10.0, global_prior=DEFAULT_PRIOR):
    buckets = defaultdict(list)
    for row in rows:
        edge = (row["state_before"], row["state_after"])
        cost = float(row["aggregate_observed_cost"])
        for ctx in context_keys(row):
            buckets[(edge, ctx)].append(cost)

    out = {}
    global_posteriors = {}

    for (edge, ctx), values in buckets.items():
        if ctx == "global":
            p = posterior(values, global_prior, alpha)
            global_posteriors[edge] = p
            out[(edge, ctx)] = {
                "n": len(values),
                "empirical_mean": mean(values),
                "posterior_mean": p,
                "stddev": pstdev(values) if len(values) > 1 else 0.0,
                "ci95": ci95(values),
            }

    for (edge, ctx), values in buckets.items():
        if ctx == "global":
            continue
        parent = global_posteriors.get(edge, global_prior)
        p = posterior(values, parent, alpha)
        out[(edge, ctx)] = {
            "n": len(values),
            "empirical_mean": mean(values),
            "posterior_mean": p,
            "stddev": pstdev(values) if len(values) > 1 else 0.0,
            "ci95": ci95(values),
            "context_delta_from_global": p - parent,
        }

    return out


def graph_for_context(agg, ctx="global", min_support=1):
    graph = defaultdict(list)
    for (edge, bucket), stats in agg.items():
        if bucket != ctx or stats["n"] < min_support:
            continue
        src, dst = edge
        graph[src].append((dst, stats["posterior_mean"]))
    return graph


def shortest_paths(graph, source):
    dist = {source: 0.0}
    pq = [(0.0, source)]
    while pq:
        cost, node = heapq.heappop(pq)
        if cost != dist[node]:
            continue
        for nxt, weight in graph.get(node, []):
            cand = cost + weight
            if cand < dist.get(nxt, float("inf")):
                dist[nxt] = cand
                heapq.heappush(pq, (cand, nxt))
    return dist


def heights_to_target(graph, target):
    reverse = defaultdict(list)
    for src, edges in graph.items():
        for dst, weight in edges:
            reverse[dst].append((src, weight))
    return shortest_paths(reverse, target)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("ndjson", type=Path)
    p.add_argument("--alpha", type=float, default=10.0)
    p.add_argument("--prior", type=float, default=DEFAULT_PRIOR)
    p.add_argument("--context", default="global")
    p.add_argument("--target", default="ACE")
    args = p.parse_args()

    rows = load_ndjson(args.ndjson)
    agg = aggregate(rows, alpha=args.alpha, global_prior=args.prior)

    print("# edge estimates")
    for (edge, ctx), stats in sorted(agg.items()):
        print(json.dumps({
            "edge": f"{edge[0]}->{edge[1]}",
            "context": ctx,
            **stats,
        }, ensure_ascii=False))

    graph = graph_for_context(agg, ctx=args.context)
    heights = heights_to_target(graph, args.target)

    print("# node heights: expected shortest posterior cost to target")
    for state, h in sorted(heights.items(), key=lambda x: x[1]):
        print(json.dumps({"state": state, "target": args.target, "height": h}))


if __name__ == "__main__":
    main()
