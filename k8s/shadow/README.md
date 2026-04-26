# Shadow Deployment

**Goal:** Run the new version alongside the primary, but **send it a copy of
real traffic without returning its responses to users**. Great for testing
performance, logging, and crash behavior under real load — zero user impact
even if shadow blows up.

## Apply

```bash
kubectl apply -f k8s/shadow/
minikube service aceest-fitness --url           # primary — returns 3.1.2
kubectl get svc aceest-fitness-shadow           # shadow — ClusterIP only
```

`aceest-fitness` (NodePort) serves users → `role=primary` pods.
`aceest-fitness-shadow` (internal-only) → `role=shadow` pods.

## Mirroring traffic

Full mirroring requires a service mesh (Istio `VirtualService` with
`mirror:`) or an nginx reverse proxy. Without a mesh, a common k8s-native
approximation is a **sidecar / tap** that copies requests, or an external
load generator that fires production-replayed traffic at the shadow service.

### Quick demo without a mesh

Send synthetic traffic to shadow from the primary's pod (simulates mirroring):

```bash
PRIMARY_POD=$(kubectl get pod -l role=primary -o jsonpath='{.items[0].metadata.name}')
kubectl exec -it $PRIMARY_POD -- sh -c \
  'for i in 1 2 3 4 5; do wget -qO- http://aceest-fitness-shadow/version; echo; done'
# Expect: 3.2.4 printed 5 times
```

## Inspect shadow logs after a load test

```bash
kubectl logs -l role=shadow --tail=50
# Watch for 5xx, slow requests, or memory/CPU pressure
```

## Why this matters

- **No user impact** — shadow responses are never returned; a bug in v3.2.4
  can't break any customer's request
- **Production-grade load testing** — you see the new version under the
  exact traffic shape it'll get when promoted
- **Pairs with metrics** — prometheus latency histograms for primary vs
  shadow tell you if the new version is slower before you cut over
