# Backstage Helm wrapper

This chart wraps the official Backstage Helm chart, pinned to version `2.10.2`,
the latest version available when this wrapper was created. The upstream chart
deploys its pre-packaged `ghcr.io/backstage/backstage:latest` demo image.

The demo image is useful to try Backstage, but is not recommended for
production. Build and use a custom Backstage image for production deployments.
PostgreSQL is disabled by default; configure a persistent, production-ready
database before using Backstage for durable data.

Argo CD discovers this chart under `deploy/helm/argocd/backstage` and deploys it
in its own `backstage` namespace, in a dedicated RollingSync step.
