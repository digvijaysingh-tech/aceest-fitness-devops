# Blue-Green Deployment

**Goal:** Keep the old version (**blue**) running while you deploy the new
version (**green**). Flip traffic in one atomic step by changing the service
selector.

## Apply both

```bash
kubectl apply -f k8s/blue-green/
minikube service aceest-fitness --url    # service points to blue
curl $(minikube service aceest-fitness --url)/version   # -> 3.1.2
```

## Switch traffic blue -> green (cutover)

```bash
kubectl patch service aceest-fitness -p '{"spec":{"selector":{"app":"aceest-fitness","color":"green"}}}'
curl $(minikube service aceest-fitness --url)/version   # -> 3.2.4
```

## Rollback (green -> blue)

```bash
kubectl patch service aceest-fitness -p '{"spec":{"selector":{"app":"aceest-fitness","color":"blue"}}}'
```

## Clean up the idle color

Once green is validated:

```bash
kubectl scale deployment aceest-fitness-blue --replicas=0
# or: kubectl delete -f k8s/blue-green/deployment-blue.yaml
```

## Why this matters

- **Zero request loss** during cutover (selector swap is instant)
- **Instant rollback** — blue is still running at full capacity
- **Easy to test green** before cutover by port-forwarding directly:
  ```bash
  kubectl port-forward deployment/aceest-fitness-green 8000:5000
  curl http://localhost:8000/version
  ```
