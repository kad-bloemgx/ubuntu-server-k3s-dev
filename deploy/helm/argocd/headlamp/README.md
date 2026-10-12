# Headlamp

Headlamp is deployed in the `headlamp` namespace and exposed through Traefik at
`https://headlamp.gerardbloemendaal.freemyip.com`.

The chart creates a separate `headlamp-user` service account and binds it to the
`headlamp-cluster-reader`
ClusterRole. It grants `get`, `list`, and `watch` on the API resources currently
installed in the cluster, including Secrets, across all namespaces. It does not
grant write verbs or access to sensitive `nodes/proxy` subresources. Kubernetes
RBAC cannot allow reading Secret names while hiding their contents: this role
can read Secret data. Its resource list should be updated when new API
resources or CRDs are installed. The dashboard pod keeps its separate
`headlamp` service account and does not receive this user role.

Create a short-lived token for the `headlamp-user` service account and use it to
sign in to Headlamp:

```bash
kubectl create token headlamp-user -n headlamp
```

Treat the token as a credential: anyone holding it can read the listed resources,
including Secret data, cluster-wide.

## No in-flight request limit

Every other app in this repository caps the number of concurrent requests per
client IP through a Traefik `inFlightReq` middleware. Headlamp deliberately
does not.

Headlamp keeps an open `?watch=1` connection per resource type per namespace.
Those connections live for as long as the browser tab is open; the access log
showed individual requests lasting over 450 seconds. Traefik counts each of
them as in flight, so Headlamp crossed the limit of 100 on its own and every
further request was answered with HTTP 429 straight away. The browser then
reports "Lost connection to the cluster".

The limit used to sit on the websecure entrypoint, which applies to every
router and allows no exceptions. It now lives in each app chart instead, under
`inFlightReq` in `values.yaml`, so this chart can leave it out. Rate limiting
and the security headers still apply here, since those come from the
entrypoint.

Verify that Traefik sees no in-flight middleware on this router:

```bash
curl -s http://192.168.1.26:8081/api/http/routers | \
  jq -r '.[] | select(.name | startswith("headlamp")) | "\(.name) \(.middlewares)"'
```
