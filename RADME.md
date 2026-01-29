[index](https://kad-bloemgx.github.io/ubuntu-server-k3s-dev/index.yaml)

## Handige helm commands


- helm repo list
- helm repo add ubuntu-server-k3s-dev https://kad-bloemgx.github.io/ubuntu-server-k3s-dev
- helm search repo ubuntu-server-k3s-dev
- helm repo update
- helm install traefik ubuntu-server-k3s-dev/traefik
- 
## Specifiek voor Traefik

### Traefik Custom Resources (CRD)
```bash
kubectl config use-context k3s-bunker-02
kubectl apply -f https://raw.githubusercontent.com/traefik/traefik/v3.2/docs/content/reference/dynamic-configuration/kubernetes-crd-definition-v1.yml
kubectl apply -f https://raw.githubusercontent.com/traefik/traefik/v3.2/docs/content/reference/dynamic-configuration/kubernetes-crd-rbac.yml
```



