# Java demo

Small Java HTTP service for the Backstage catalog and graph. Requires JDK 17+
and Maven 3.9+; regenerating its library catalog also requires Python 3. It
uses the JDK HTTP server with no runtime dependencies.
This example is local only: no container, Helm chart or Argo CD deployment is
created.

From the repository root:

```bash
mvn -f examples/java-demo/pom.xml verify
java -jar examples/java-demo/target/java-demo-1.0.0-SNAPSHOT.jar
```

In another terminal:

```bash
curl --fail http://127.0.0.1:8080/api/greeting
```

The response is `{"message":"Hello from Java demo"}`. The service binds only to
`127.0.0.1`; stop it with Ctrl+C. An optional port argument overrides 8080:

```bash
java -jar examples/java-demo/target/java-demo-1.0.0-SNAPSHOT.jar 8081
```

Only `GET /api/greeting` is supported. Other methods return 405 with `Allow:
GET`; unknown paths return 404. `openapi.yaml` describes the default local URL;
adjust it when trying a different port.

## Backstage graph

The root `catalog-info.yaml` registers `component:default/java-demo` and
`api:default/java-demo-api`. The API definition is loaded from this directory's
`openapi.yaml`, so publish both files to `main`.

After Argo CD rolls out the updated Backstage values (which allow `API` entities)
and Backstage refreshes the catalog, open `/catalog-graph`. Select Java Demo and
include `API`, `System` and `User` kinds and `providesApi`, `partOf` and `ownedBy`
relations in the graph filters. You can then see:

- Java Demo **provides** Java Demo Greeting API.
- Both entities **belong to** Ubuntu Server K3s Platform.
- Both entities **are owned by** Gerard Bloemendaal.

Registering the API does not start the service.

## Maven library graph

The service has no runtime dependencies, but Maven resolves JUnit and its
transitive libraries for tests. `tools/generate_catalog.py` runs the pinned
`org.apache.maven.plugins:maven-dependency-plugin:3.8.1:tree` goal with JSON
output and no scope filter, then writes two generated files:

- `catalog-dependencies.yaml`: Java Demo's direct dependencies, loaded into its
  `spec.dependsOn` through `$yaml` in the root `catalog-info.yaml`.
- `catalog-libraries.yaml`: one `Component` of type `library` per resolved
  artifact, with `dependsOn` edges taken from the resolved tree. The root
  `java-demo-libraries` `Location` registers this file.

Each library is identified by its Maven coordinates (group, artifact, version,
type and classifier); its entity name is a stable, hashed name such as
`maven-junit-jupiter-9ce8fda69db5`. The `maven.apache.org/coordinates` and
`maven.apache.org/scopes` annotations and `maven-scope-*` tags record every
scope Maven reported. Test-only libraries say so in their description:
`dependsOn` includes test dependencies, so check the scope before treating an
edge as a runtime dependency. Maven omits repeated artifacts from its tree, so
only the edges Maven reports are shown. The owner,
`user:default/gerard-bloemendaal`, is the catalog steward for these entries, not
the upstream library author.

Regenerating requires Python 3, Maven 3.9+ and a JDK. From the repository root:

```bash
python3 examples/java-demo/tools/generate_catalog.py
python3 -m unittest discover -s examples/java-demo/tools
```

Pass `--settings path/to/settings.xml` to use specific Maven settings, or
`--dependency-tree tree.json` to generate from an existing `dependency:tree`
JSON file without running Maven. `--check` writes nothing and exits non-zero
when the generated files are stale. Only this demo's `pom.xml` is supported.
Commit the regenerated files with the `pom.xml` change and push them to `main`.
The `java-demo-catalog` GitHub Actions workflow runs the tests, `--check` and
`mvn verify`; it fails on stale files but never commits or deploys anything.

After Backstage refreshes the catalog, open Java Demo in `/catalog-graph` and
add the `dependsOn` and `dependencyOf` relations with the `Component` kind to
the graph filters. Increase the depth to show transitive libraries.
