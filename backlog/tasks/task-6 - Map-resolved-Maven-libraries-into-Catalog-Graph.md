---
id: TASK-6
title: Map resolved Maven libraries into Catalog Graph
status: Done
assignee:
  - '@Copilot'
created_date: '2026-10-13 14:13'
updated_date: '2026-10-13 14:20'
labels: []
dependencies: []
modified_files:
  - examples/java-demo/tools/generate_catalog.py
  - examples/java-demo/catalog-dependencies.yaml
  - examples/java-demo/catalog-libraries.yaml
  - examples/java-demo/tools/test_generate_catalog.py
  - examples/java-demo/.gitignore
  - catalog-info.yaml
  - deploy/helm/argocd/backstage/values.yaml
  - .github/workflows/java-demo-catalog.yml
  - examples/java-demo/README.md
  - deploy/helm/argocd/backstage/README.md
type: feature
ordinal: 6000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
User requests automatic mapping of Java-demo Maven dependencies into library nodes and dependsOn graph relationships. Scope explicitly includes direct and transitive dependencies and tests, with labels distinguishing test scope from runtime. Catalog descriptors must be generated from Maven resolution, not inferred from pom.xml or hardcoded.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 A generator uses Maven resolved dependency-tree JSON to produce stable library entities and app/library dependsOn edges for direct and transitive dependencies, including tests with explicit scope metadata.
- [x] #2 Root catalog ingests generated library nodes and Java Demo references without duplicate component ownership; all generated entity schemas and reference targets validate.
- [x] #3 Tests cover generation, shared dependencies/scopes, coordinate identity, invalid input and stale-output detection; Maven resolution confirms the actual demo library set.
- [x] #4 Documentation and CI explain regeneration, drift checking and graph filters, with no automatic dependency deployment.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Implement a standard-library Python generator using pinned Maven dependency plugin JSON output and deterministic YAML-compatible JSON files; add focused tests.
2. Wire generated dependency references and library location into root catalog and allow Location ingestion at its configured location.
3. Generate real demo library catalog, add CI drift checks and document local regeneration.
4. Run generator tests, real Maven resolution/build, official Backstage schema/reference checks and Helm rendering.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Generator: examples/java-demo/tools/generate_catalog.py runs pinned maven-dependency-plugin:3.8.1:tree (JSON, no scope filter), validates root nl.kadaster.demo:java-demo, keys/types/coordinates/scopes/optional/children, dedups by group:artifact:version:type:classifier with sha256-hashed names <=63 chars, merges scopes/edges for shared nodes, writes JSON-in-YAML outputs; empty trees produce [] and a comment-only (no entity) library file. Library owner documents catalog stewardship only. Root catalog: java-demo spec.dependsOn via $yaml; Location java-demo-libraries targets generated libraries. Helm per-location rule now allows Location (global rule already did).

Validation: real Maven resolution (temporary central-mirror settings, deleted afterwards) produced 8 test-scoped libraries, 1 direct app edge + 7 library edges; regeneration byte-identical (md5 unchanged); --check rc 0 when current, rc 1 on drift without writing; offline --dependency-tree --check rc 0; python3 -m unittest discover -s examples/java-demo/tools: 9 tests OK; mvn verify: 4 tests, 0 failures. Live Backstage catalog-model (SchemaValid/FieldFormat/NoForeignRootFields policies + Component/API/System/User/Location validators) validated 19 entities after resolving $yaml/$text and Location target: no duplicates, 0 dangling refs; negative control (dangling ref, bad type) failed as expected. helm lint OK; template diff vs original only adds Location to per-location rules and app-config checksum; guest auth, pg DB, reading.allow, existingSecret preserved. Workflow YAML parsed; action tags checkout@v5, setup-java@v5, setup-python@v6 verified to exist. No commit, push or deploy.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added a stdlib Python generator that maps Java Demo's Maven-resolved dependency tree (direct, transitive and test scopes) to library Components with dependsOn edges, wired into the root catalog via $yaml and a Location, plus unit tests, a read-only drift-check CI workflow and docs. Verified with 9 unit tests, real Maven generation/--check (8 test-scoped libraries, 8 dependsOn edges), mvn verify, official Backstage validators with reference checks, and Helm lint/render diff.
<!-- SECTION:FINAL_SUMMARY:END -->
