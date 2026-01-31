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

## Specifiek voor Traefik

### Traefik Custom Resources (CRD) voor versie 3.6.7

```bash
kubectl apply -f https://raw.githubusercontent.com/traefik/traefik/v3.6.7/docs/content/reference/dynamic-configuration/kubernetes-crd-definition-v1.yml
kubectl apply -f https://raw.githubusercontent.com/traefik/traefik/v3.6.7/docs/content/reference/dynamic-configuration/kubernetes-crd-rbac.yml
```



