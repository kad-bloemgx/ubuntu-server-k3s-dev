# PostgreSQL

Deze Helm-chart wordt via Argo CD uitgerold in namespace `postgresql`.
Het is een wrapper rond de Bitnami-chart `postgresql`.

Wachtwoorden staan niet in git. Ze komen uit de handmatig aangemaakte Secret
`postgresql-credentials` met de keys `postgres-password` en `password`.

## NetworkPolicy

De Bitnami-chart maakt zelf een NetworkPolicy aan. Standaard staat die alle
inkomend verkeer op poort 5432 toe. In `values.yaml` is daarom
`primary.networkPolicy.allowExternal` op `false` gezet, waardoor alleen de
expliciet benoemde bronnen de database mogen benaderen:

- pods in de namespace `postgresql` zelf;
- pods in de namespace `postgresql` met het label `postgresql-client: "true"`;
- alle pods in de namespace `pgadmin`, via `primary.networkPolicy.extraIngress`.

Egress blijft open (`allowExternalEgress: true`), zodat de pod onder andere
DNS kan blijven benaderen.

Een extra namespace toegang geven doe je door een namespaceSelector toe te
voegen aan `primary.networkPolicy.extraIngress`:

```yaml
extraIngress:
  - ports:
      - port: 5432
        protocol: TCP
    from:
      - namespaceSelector:
          matchLabels:
            kubernetes.io/metadata.name: pgadmin
      - namespaceSelector:
          matchLabels:
            kubernetes.io/metadata.name: nextcloud
```

Het label `kubernetes.io/metadata.name` wordt door Kubernetes automatisch op
elke namespace gezet en komt overeen met de namespacenaam.

### Controleren

Vanuit een willekeurige andere namespace moet de verbinding mislukken:

```bash
kubectl run netpol-test --rm -i --restart=Never --image=busybox:1.36 -n default \
  --command -- nc -z -w3 postgresql.postgresql.svc.cluster.local 5432
```

Vanuit `pgadmin` moet de verbinding slagen:

```bash
kubectl run netpol-test --rm -i --restart=Never --image=busybox:1.36 -n pgadmin \
  --command -- nc -z -w3 postgresql.postgresql.svc.cluster.local 5432
```
