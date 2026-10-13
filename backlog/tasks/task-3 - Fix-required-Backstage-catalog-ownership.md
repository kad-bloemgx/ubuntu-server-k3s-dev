---
id: TASK-3
title: Fix required Backstage catalog ownership
status: Done
assignee:
  - '@Copilot'
created_date: '2026-10-13 12:56'
updated_date: '2026-10-13 12:57'
labels: []
dependencies: []
modified_files:
  - catalog-info.yaml
  - deploy/helm/argocd/backstage/values.yaml
  - deploy/helm/argocd/backstage/README.md
type: bug
ordinal: 3000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The initial catalog descriptor omitted mandatory spec.owner on System and Component entities. The user confirmed Gerard Bloemendaal should be represented as a User and own these entities.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 All System and Component entities specify user:default/gerard-bloemendaal as owner, and a valid matching User entity exists.
- [x] #2 The configured catalog location permits User ingestion and documentation describes required ownership.
- [x] #3 All descriptor entities pass official Backstage entity schema validation.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add Gerard Bloemendaal as a User and reference that user from all required owner fields.
2. Allow User at the configured location and document ownership.
3. Validate descriptors against official Backstage schemas and render/lint Helm.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Validated all eight YAML entities with installed @backstage/catalog-model User/System/Component kind validators in the running demo container, without modifying cluster resources. Asserted required owner references and matching User existence. Helm lint and rendered ConfigMap assertions passed: location permits System, Component, User; guest auth and pg retained. git diff --check passed. README documents required fields and distinguishes catalog ownership from guest login. Changes remain local; publish to main and sync via Argo CD to ingest.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Corrected missing mandatory ownership, registered Gerard Bloemendaal as a User, allowed User ingestion, and documented ownership. All eight entities pass official Backstage kind-schema validators; Helm lint and rendered config checks passed. Not deployed.
<!-- SECTION:FINAL_SUMMARY:END -->
