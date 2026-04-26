# Rolling Update

**Goal:** Update pods one-at-a-time with zero downtime. Default k8s strategy.

## Apply

```bash
kubectl apply -f k8s/rolling-update/
minikube service aceest-fitness --url
```

## Demo an update

Simulate rolling out v3.2.4 → an "imaginary v3.3.0" (same image, re-tag to prove the mechanism):

```bash
kubectl set image deployment/aceest-fitness \
  aceest-fitness=dshekhawat06640/aceest-fitness:3.1.2

kubectl rollout status deployment/aceest-fitness
kubectl get pods -l app=aceest-fitness -w
```

## Rollback

```bash
kubectl rollout undo deployment/aceest-fitness
kubectl rollout history deployment/aceest-fitness
```

## Why this matters

`maxSurge: 1, maxUnavailable: 0` means k8s creates 1 new pod before killing an
old one — always ≥ 4 healthy pods. No downtime during updates.
