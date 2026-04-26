# Canary Release

**Goal:** Send a small percentage of traffic to the new version (canary).
If it's healthy, grow it; if not, kill it.

The service selector matches `app=aceest-fitness` **without** a track filter,
so k8s load-balances across BOTH deployments. With 4 stable + 1 canary pods,
~20% of requests hit the canary.

## Apply

```bash
kubectl apply -f k8s/canary/
minikube service aceest-fitness --url
```

## Verify traffic split (~20%)

Hit `/version` repeatedly and count:

```bash
URL=$(minikube service aceest-fitness --url)
for i in $(seq 1 50); do curl -s $URL/version; echo; done | sort | uniq -c
# Expect roughly: ~40 "3.1.2", ~10 "3.2.4"
```

## Promote canary to stable (ramp up)

```bash
kubectl scale deployment aceest-fitness-canary --replicas=4
kubectl scale deployment aceest-fitness-stable --replicas=0
```

## Abort canary (rollback)

```bash
kubectl scale deployment aceest-fitness-canary --replicas=0
```

## Why this matters

- **Limits blast radius** — a bad canary only breaks ~20% of users
- **Real production metrics** — you see error rates in anger, not just in staging
- **Controlled ramp** — adjust replica ratio to shift traffic gradually (1:4 -> 1:1 -> 4:1)
