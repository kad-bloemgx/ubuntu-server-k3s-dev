# README

## GitHub pages 

[index](https://kad-bloemgx.github.io/ubuntu-server-k3s-dev/index.yaml)

## Handige helm commands

```bash
helm repo list
```

```bash
helm repo add ubuntu-server-k3s-dev https://kad-bloemgx.github.io/ubuntu-server-k3s-dev
```

```bash
helm search repo ubuntu-server-k3s-dev
```

```bash
helm repo update
```

```bash
helm install traefik ubuntu-server-k3s-dev/traefik
```

## Backstage

Argo CD ontdekt de Backstage-wrapper onder `deploy/helm/argocd/backstage` en
rolt die uit in een eigen synchronisatiestap nadat de voorgaande stappen zijn
voltooid. De wrapper gebruikt de officiële Backstage-chart `2.10.2` met de
upstream demo-image `ghcr.io/backstage/backstage:latest`. Deze image is bedoeld
om Backstage uit te proberen, niet voor productie.

```bash
helm template backstage ./deploy/helm/argocd/backstage \
  --namespace backstage
```

De chart is configureerbaar met de upstream-waarden onder `backstage:` in
`deploy/helm/argocd/backstage/values.yaml`. Gebruik voor productie een eigen
gebouwde image en configureer een persistente database.

## Specifiek voor Traefik

### Traefik Custom Resources (CRD) voor versie 3.6.7

```bash
kubectl apply -f https://raw.githubusercontent.com/traefik/traefik/v3.6.7/docs/content/reference/dynamic-configuration/kubernetes-crd-definition-v1.yml
kubectl apply -f https://raw.githubusercontent.com/traefik/traefik/v3.6.7/docs/content/reference/dynamic-configuration/kubernetes-crd-rbac.yml
```
