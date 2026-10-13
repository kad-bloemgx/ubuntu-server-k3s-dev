---
id: TASK-1
title: Add repository software catalog to Backstage
status: Done
assignee:
  - Gerard Bloemendaal
created_date: '2026-10-13 11:11'
updated_date: '2026-10-13 11:13'
labels: []
dependencies: []
modified_files:
  - catalog-info.yaml
  - deploy/helm/argocd/backstage/values.yaml
  - deploy/helm/argocd/backstage/README.md
priority: medium
type: feature
ordinal: 1000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The Backstage installation currently uses the upstream demo catalog, while this repository deploys its own Kubernetes platform and Helm-managed applications through Argo CD. Users need a catalog that represents this repository and the applications maintained and deployed here.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Backstage loads catalog entities describing this repository and the Helm charts discovered under deploy/helm/argocd (Argo CD, Backstage, Headlamp, demo-app, and storage).
Entities accurately reference their source paths in this repository and are grouped under a platform system.
- [x] #2 The Backstage deployment config registers the catalog descriptor from this repository without removing the existing database and auth configuration.
- [x] #3 The Backstage README explains the catalog source and how to add or update an entity.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add a root catalog descriptor for the repository, its platform system, and each current chart under deploy/helm/argocd.
2. Register the descriptor as a URL catalog location in the Backstage Helm wrapper appConfig, preserving existing database/auth behavior.
3. Document the catalog workflow and verify the rendered Helm configuration and descriptor structure.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Validation passed: helm lint reported zero chart failures; helm template rendered the catalog URL and retained backend.database.client=pg and the existing config-file arguments; yq parsed all 7 catalog documents and confirmed all 6 components reference ubuntu-server-platform; git diff --check passed. Runtime catalog ingestion will occur once this change is merged to main.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added catalog-info.yaml for the repository, platform system, and five Helm-managed chart components; configured Backstage to fetch it from GitHub; documented catalog maintenance and corrected the PostgreSQL README description. Verified with helm lint, helm template, yq, and git diff --check.
<!-- SECTION:FINAL_SUMMARY:END -->
