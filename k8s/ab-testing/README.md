# A/B Testing

**Goal:** Two variants running side-by-side with **separate stable URLs**.
Users (or a front-end router / feature flag) decide which to hit. Unlike
canary, A/B isn't about "safer rollout" — it's about comparing behavior of
two versions head-to-head on real users.

## Apply

```bash
kubectl apply -f k8s/ab-testing/
```

## Get both URLs

```bash
minikube service aceest-fitness-a --url    # variant A (v3.1.2)
minikube service aceest-fitness-b --url    # variant B (v3.2.4)
```

Each service is pinned to its variant via `variant: a` / `variant: b` selector.

## Demo

```bash
A=$(minikube service aceest-fitness-a --url)
B=$(minikube service aceest-fitness-b --url)
curl $A/version   # {"version":"3.1.2"}
curl $B/version   # {"version":"3.2.4"}
```

## In a real deployment

A gateway (nginx / Istio VirtualService / application code) routes users
based on a cookie, header, or percentage — e.g. users in the `beta` cohort
always hit variant B, everyone else hits A.

## Why this matters

- **Behavior comparison** — you see whether v3.2.4 improves signup conversion,
  retention, etc. compared to v3.1.2 on the same user base
- **Stable assignment** — unlike canary's random split, users keep getting
  the same variant across requests
