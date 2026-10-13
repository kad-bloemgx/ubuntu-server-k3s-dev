---
id: TASK-2
title: Enable token-based Backstage guest authentication
status: Done
assignee:
  - '@Copilot'
created_date: '2026-10-13 11:26'
updated_date: '2026-10-13 11:26'
labels: []
dependencies: []
modified_files:
  - deploy/helm/argocd/backstage/values.yaml
  - deploy/helm/argocd/backstage/README.md
type: bug
ordinal: 2000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Guest sign-in fails against the auth backend and the permission authorize endpoint returns 401 Missing credentials. The user requests guest authentication for this demo deployment and has been informed that this allows anonymous access.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Rendered Backstage app config enables auth.providers.guest.dangerouslyAllowOutsideDevelopment while preserving database and catalog settings.
- [x] #2 README documents anonymous access, deployment steps, and signing in without the legacy guest-token fallback.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Explicitly enable the guest provider outside development in Helm appConfig.
2. Document test-only access and rollout/login instructions.
3. Validate rendered configuration and chart lint; verify live login only if a reachable deployment is available.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Confirmed live cause with GET /api/auth/guest/refresh inside the running pod: HTTP 403 NotAllowedError explicitly requires auth.providers.guest.dangerouslyAllowOutsideDevelopment. Enabled that exact setting in repository config. helm lint passed; rendered ConfigMap assertions confirmed guest flag=true, database client=pg, and unchanged catalog URL; git diff --check passed. README reviewed for anonymous-access warning and rollout/re-login instructions. Changes are local only; no cluster configuration was modified and successful post-rollout login is not yet verified.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Enabled token-based guest auth outside development in Helm values and documented demo-only anonymous access. Verified rendered settings and chart lint; live backend confirmed the missing flag causes the current 403. Publish and Argo CD rollout remain required before guest login is active.
<!-- SECTION:FINAL_SUMMARY:END -->
