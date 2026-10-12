# Headlamp

Headlamp is deployed in the `headlamp` namespace and exposed through Traefik at
`https://headlamp.gerardbloemendaal.freemyip.com`.

The chart deliberately does not bind the Headlamp service account to
`cluster-admin` and does not enable service-account-token authentication.
Authenticate in Headlamp with a Kubernetes user token that has only the access
you need. The built-in Kubernetes `view` role is a suitable read-only starting
point; it does not grant access to Secret data. Do not grant `get`, `list`, or
`watch` on Secrets unless users should be able to read their values.

Kubernetes RBAC cannot allow reading Secret names while hiding their contents:
permission to read a Secret also grants its data. Avoid exposing the dashboard
publicly without an additional access-control layer.

## Create a read-only login token

The `headlamp` service account has no cluster permissions by default. To grant
it read-only access to resources covered by the built-in `view` role, create a
cluster-wide binding:

```bash
kubectl create clusterrolebinding headlamp-view \
  --clusterrole=view \
  --serviceaccount=headlamp:headlamp
```

Then create a short-lived token and use it to sign in to Headlamp:

```bash
kubectl create token headlamp -n headlamp
```

The `view` role does not grant access to Secret data. Treat the token as a
credential and do not share or store it in an unsecured location. For access
limited to specific namespaces, use a `RoleBinding` in each namespace instead
of a cluster-wide binding.

## Grant access to Secrets

Only grant this when Secret values need to be visible. Anyone with these
permissions can read the Secret contents in the namespace. Apply a namespaced
Role and RoleBinding for each namespace that should be accessible:

```bash
kubectl create clusterrole headlamp-secrets-reader \
  --verb=get,list,watch \
  --resource=secrets
  

kubectl create clusterrolebinding headlamp-secrets-reader \
  --clusterrole=headlamp-secrets-reader \
  --serviceaccount=headlamp:headlamp
```

```bash
kubectl create token headlamp -n headlamp
```

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
