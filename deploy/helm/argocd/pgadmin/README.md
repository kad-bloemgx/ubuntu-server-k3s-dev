# pgAdmin

Deze Helm-chart wordt via Argo CD uitgerold in namespace `pgadmin`.
Het is een wrapper rond de chart `pgadmin4`.

De PostgreSQL-server wordt automatisch geregistreerd via `serverDefinitions`.
Het wachtwoord komt uit een gemount pgpass-bestand (Secret `postgresql-pgpass`)
en het loginwachtwoord uit de Secret `pgadmin-credentials`. Beide Secrets zijn
handmatig aangemaakt en staan niet in git.

## NetworkPolicy

De `pgadmin4`-chart maakt zelf een NetworkPolicy aan, maar die laat al het
verkeer op de containerpoort toe. Die policy is uitgeschakeld
(`pgadmin4.networkPolicy.enabled: false`) en vervangen door
`templates/networkpolicy.yaml`, dat twee policies aanmaakt:

1. `pgadmin-default-deny-ingress`: blokkeert al het inkomend verkeer naar elke
   pod in de namespace.
2. `pgadmin-allow-ingress`: staat verkeer naar de pgAdmin-pods toe vanuit de
   namespaces in `networkPolicy.allowedIngressNamespaces`.

Standaard is alleen `traefik` toegestaan, zodat pgAdmin uitsluitend via de
IngressRoute bereikbaar is en niet rechtstreeks vanuit andere namespaces.

```yaml
networkPolicy:
  enabled: true
  targetPort: 80
  allowedIngressNamespaces:
    - traefik
```

Het label `kubernetes.io/metadata.name` wordt door Kubernetes automatisch op
elke namespace gezet en komt overeen met de namespacenaam.

De policies regelen alleen ingress. Uitgaand verkeer van pgAdmin naar
PostgreSQL blijft toegestaan; dat verkeer wordt aan de andere kant beperkt
door de NetworkPolicy in de chart `postgresql`.

### Controleren

Vanuit een willekeurige andere namespace moet de verbinding mislukken:

```bash
kubectl run netpol-test --rm -i --restart=Never --image=busybox:1.36 -n default \
  --command -- nc -z -w3 pgadmin.pgadmin.svc.cluster.local 80
```

Vanuit `traefik` moet de verbinding slagen:

```bash
kubectl run netpol-test --rm -i --restart=Never --image=busybox:1.36 -n traefik \
  --command -- nc -z -w3 pgadmin.pgadmin.svc.cluster.local 80
```
