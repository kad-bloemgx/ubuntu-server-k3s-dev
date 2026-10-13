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

## Software catalog

Backstage loads the catalog from the repository's root `catalog-info.yaml`
through a public GitHub URL. The catalog contains this repository, the
`ubuntu-server-platform` system, and components for the Argo CD, Backstage,
Headlamp, demo-app, and storage charts.

To add or update an entry, edit `catalog-info.yaml` and commit the change to
`main`. Components should reference the `ubuntu-server-platform` system and
include a `backstage.io/source-location` annotation pointing to their source
directory. The catalog location is configured in this chart's `values.yaml`.
