# Kubernetes Deployment Strategies

Five progressive-delivery strategies for the ACEest Fitness & Gym Flask app.
Each subfolder is self-contained — apply one at a time, never mix.

| Strategy | Use case | NodePort | Image mix |
|---|---|---|---|
| [rolling-update/](rolling-update/) | Default; zero-downtime incremental rollout | 30080 | Single version |
| [blue-green/](blue-green/) | Instant cutover + instant rollback | 30081 | `3.1.2` (blue) & `3.2.4` (green) |
| [canary/](canary/) | Send small % of traffic to new version first | 30082 | `3.1.2` (stable) + `3.2.4` (canary) |
| [ab-testing/](ab-testing/) | Two variants, separate URLs, behavior comparison | 30083 (A), 30084 (B) | `3.1.2` (A) vs `3.2.4` (B) |
| [shadow/](shadow/) | Mirror real traffic to new version, drop responses | 30085 (primary) | `3.1.2` (primary), `3.2.4` (shadow, internal) |

## Start Minikube once

```bash
minikube start --driver=docker --cpus=2 --memory=3g
minikube addons enable metrics-server
```

## Switch between strategies cleanly

Different strategies use the same service name (`aceest-fitness`) but
different selectors. To avoid leftovers, wipe between demos:

```bash
kubectl delete deploy,svc -l app=aceest-fitness
kubectl apply -f k8s/<strategy>/
```

## Rollback — common to all

```bash
kubectl rollout undo deployment/<name>
kubectl rollout history deployment/<name>
```

For blue-green, "rollback" is a service selector patch (see that folder's README).
