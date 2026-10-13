---
id: TASK-4
title: Allow Backstage catalog reads and User registration
status: Done
assignee:
  - '@Copilot'
created_date: '2026-10-13 13:25'
updated_date: '2026-10-13 13:26'
labels: []
dependencies: []
modified_files:
  - deploy/helm/argocd/backstage/values.yaml
  - deploy/helm/argocd/backstage/README.md
type: bug
ordinal: 4000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Live catalog logs reject the configured raw GitHub URL as unreadable. A manually registered GitHub blob URL also rejects the User entity because global catalog rules do not allow User. User approved correcting both restrictions.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Rendered backend reading permissions allow only the configured repository main path on raw.githubusercontent.com.
- [x] #2 Rendered global catalog rules allow Component, System, Location and User while retaining per-location rules, guest auth and database settings.
- [x] #3 Documentation explains rollout and using one catalog location rather than duplicate GitHub/raw registrations.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add a repository/path-scoped backend reading allow entry and explicit global catalog kind rules.
2. Document the configured location and duplicate-location cleanup.
3. Lint and assert rendered configuration; leave deployment to the existing GitOps workflow.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
helm lint and git diff --check passed. Piped rendered appConfig into the existing demo container and constructed a separate Backstage UrlReaders instance without changing cluster configuration: configured raw URL read succeeded, parsed storage has the required owner, and a URL outside the allowed main path was rejected. Assertions verified global/per-location kind rules and unchanged guest-auth/database settings. Documentation reviewed for rollout and manual duplicate-location removal. Configuration remains local and is not deployed.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Allowed repository-scoped raw GitHub reads and User registration; documented a single configured catalog location. Verified actual Backstage URL-reader behavior with rendered config, allowed and rejected paths, preserved settings, and Helm lint. Deployment via main/Argo CD remains pending.
<!-- SECTION:FINAL_SUMMARY:END -->
