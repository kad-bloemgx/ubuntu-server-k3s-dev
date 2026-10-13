---
id: TASK-5
title: Add buildable Java demo to Backstage graph
status: Done
assignee:
  - '@Copilot'
created_date: '2026-10-13 13:43'
updated_date: '2026-10-13 13:47'
labels: []
dependencies: []
modified_files:
  - examples/java-demo/pom.xml
  - examples/java-demo/src/main/java/nl/kadaster/demo/DemoApplication.java
  - examples/java-demo/src/test/java/nl/kadaster/demo/DemoApplicationTest.java
  - examples/java-demo/openapi.yaml
  - examples/java-demo/.gitignore
  - catalog-info.yaml
  - deploy/helm/argocd/backstage/values.yaml
  - examples/java-demo/README.md
  - deploy/helm/argocd/backstage/README.md
type: feature
ordinal: 5000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
User wants a Java demo in this repository that can be displayed in Catalog Graph, explicitly without container or Kubernetes deployment. A local HTTP service and its API provide meaningful catalog relationships without inventing runtime dependencies.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Java 17 Maven demo builds and serves a documented JSON greeting endpoint with automated HTTP tests.
- [x] #2 Root catalog describes the demo Component and its OpenAPI API with valid owner/system/providesApis references; configured rules permit API ingestion.
- [x] #3 Documentation explains building, running and viewing the graph without deploying the demo.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add a dependency-light Java HTTP demo, Maven build, tests, OpenAPI and local build ignore rules.
2. Add Component/API catalog entities and allow API ingestion.
3. Document local usage and graph relations; run Maven tests, smoke test packaged JAR, validate Backstage schemas and Helm rendering.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Maven verify passed with 4 HTTP tests (greeting, unknown paths/prefixes, POST and HEAD); packaged JAR smoke test returned the documented JSON and was terminated afterwards. Local Maven mirror returned 401, so validation used temporary session-only public Maven Central settings; the file was removed and user settings were not changed. Official Backstage kind validators accepted all 10 entities with the local OpenAPI substitution resolved; all owner/system/providesApis targets resolve. Helm lint and rendered config assertions passed including API kind allowlists and preserved guest/database settings. git diff --check passed. Docs describe loopback-only execution and graph relation filters. No Kubernetes deployment or application registration was changed live; publish files and sync Backstage to ingest.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added Java 17 Maven greeting service, four HTTP tests, executable JAR build, OpenAPI contract and documentation. Wired Component/API catalog graph relationships and API ingestion rules. Verified Maven build/tests, packaged-JAR HTTP response, Backstage entity schemas/references and Helm config. Changes remain local; the demo is not deployed.
<!-- SECTION:FINAL_SUMMARY:END -->
