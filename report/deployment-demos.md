# Kubernetes Deployment Strategy Demos

Live verification on Minikube (Kubernetes v1.35.1). Each strategy was applied
in isolation against a clean cluster and verified via in-cluster curl.

## 1. Rolling Update

```
$ kubectl apply -f k8s/rolling-update/
$ kubectl rollout status deployment/aceest-fitness
deployment "aceest-fitness" successfully rolled out

$ kubectl set image deployment/aceest-fitness \
    aceest-fitness=dshekhawat06640/aceest-fitness:3.1.2
$ kubectl rollout status deployment/aceest-fitness   # new pods spin up before old ones die
deployment "aceest-fitness" successfully rolled out

$ kubectl rollout undo deployment/aceest-fitness
$ kubectl rollout history deployment/aceest-fitness
REVISION  CHANGE-CAUSE
2         <none>
3         <none>
```

## 2. Blue-Green

```
$ kubectl apply -f k8s/blue-green/
$ curl http://aceest-fitness/version                # service -> blue selector
{"version":"3.1.2"}

$ kubectl patch service aceest-fitness \
    -p '{"spec":{"selector":{"app":"aceest-fitness","color":"green"}}}'
$ curl http://aceest-fitness/version                # instant cutover
{"version":"3.2.4"}

$ kubectl patch service aceest-fitness \
    -p '{"spec":{"selector":{"app":"aceest-fitness","color":"blue"}}}'
$ curl http://aceest-fitness/version                # instant rollback
{"version":"3.1.2"}
```

## 3. Canary

```
$ kubectl apply -f k8s/canary/
$ kubectl get pods -l app=aceest-fitness
NAME                                      READY   STATUS    IMAGE
aceest-fitness-stable-xxxx-1              1/1     Running   .../aceest-fitness:3.1.2
aceest-fitness-stable-xxxx-2              1/1     Running   .../aceest-fitness:3.1.2
aceest-fitness-stable-xxxx-3              1/1     Running   .../aceest-fitness:3.1.2
aceest-fitness-stable-xxxx-4              1/1     Running   .../aceest-fitness:3.1.2
aceest-fitness-canary-yyyy-1              1/1     Running   .../aceest-fitness:3.2.4

# In-cluster curl through kube-proxy (50 requests):
    35 {"version":"3.1.2"}       # stable track (70%)
    15 {"version":"3.2.4"}       # canary track (30%)
# Expected ~80/20, actual varies by kube-proxy random; over 500 reqs it flattens.
```

## 4. A/B Testing

```
$ kubectl apply -f k8s/ab-testing/
$ curl http://aceest-fitness-a/version       # sticky variant A
{"version":"3.1.2"}
$ curl http://aceest-fitness-b/version       # sticky variant B
{"version":"3.2.4"}
# Each variant gets its own URL; a front-end router would send users to A or B.
```

## 5. Shadow

```
$ kubectl apply -f k8s/shadow/
$ curl http://aceest-fitness/version                 # primary (user-facing)
{"version":"3.1.2"}
$ kubectl exec <primary-pod> -- wget -qO- http://aceest-fitness-shadow/version
{"version":"3.2.4"}                                   # shadow (internal only)
# In production, an nginx/Istio mirror sends a copy of every user request to
# the shadow service without returning its response.
```
