# Backstage Helm wrapper

This chart wraps the official Backstage Helm chart, pinned to version `2.10.2`,
the latest version available when this wrapper was created. The upstream chart
deploys its pre-packaged `ghcr.io/backstage/backstage:latest` demo image.

The demo image is useful to try Backstage, but is not recommended for
production. Build and use a custom Backstage image for production deployments.
The wrapper enables PostgreSQL with persistent storage; credentials are read
from the existing `backstage-postgresql` Secret.

Argo CD discovers this chart under `deploy/helm/argocd/backstage` and deploys it
in its own `backstage` namespace, in a dedicated RollingSync step.

## Guest authentication

The wrapper enables token-based guest sign-in with
`auth.providers.guest.dangerouslyAllowOutsideDevelopment: true`. This allows
anyone who can reach Backstage to sign in without credentials. Use it only in
a restricted demo environment, not a publicly accessible production deployment.
For production, remove this override and configure a real authentication
provider.

Publish the configuration change to `main` and let Argo CD sync the Backstage
application and roll out the updated pod. Then sign out or open a private browser
window and sign in as a guest again. Do not use the legacy guest-token fallback:
it does not provide the backend credentials required by the permission API.

## Software catalog

Backstage loads the catalog from the repository's root `catalog-info.yaml`
through a public GitHub URL. The catalog contains this repository, the
`ubuntu-server-platform` system, and components for the Argo CD, Backstage,
Headlamp, demo-app, and storage charts. A local-only
[Java demo](../../../../examples/java-demo/README.md) and its OpenAPI API are
also included for exploring Catalog Graph. A `Location` entity in the root file
registers the demo's generated Maven library components; do not edit those
generated files by hand.
Gerard Bloemendaal is registered as a `User` and owns the system and components
through `spec.owner: user:default/gerard-bloemendaal`. This catalog identity is
separate from guest authentication; it does not create a login account.

To add or update an entry, edit `catalog-info.yaml` and commit the change to
`main`. Components should reference the `ubuntu-server-platform` system and
include a `backstage.io/source-location` annotation pointing to their source
directory. Components require `spec.type`, `spec.lifecycle`, and `spec.owner`;
systems also require `spec.owner`. The catalog location in this chart's
`values.yaml` allows `System`, `Component`, `User`, `API`, and `Location`
entities.

The backend's `reading.allow` permits raw GitHub reads only under
`/kad-bloemgx/ubuntu-server-k3s-dev/main/`. Global `catalog.rules` also allow
`Component`, `System`, `Location`, `User`, and `API`, so manual registration can
ingest the owner and API entities.

After publishing configuration changes to `main`, let Argo CD sync and roll out
Backstage before refreshing the catalog. The raw GitHub URL is already
registered through configuration; do not register the same file again using
the GitHub `blob/main` URL. If that duplicate location was registered manually,
unregister only that manual location in Backstage, keeping the configured raw
location, then refresh the configured location to reprocess its entities.
