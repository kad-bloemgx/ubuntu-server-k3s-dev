# Java demo

Small Java HTTP service for the Backstage catalog and graph. Requires JDK 17+
and Maven 3.9+. It uses the JDK HTTP server with no runtime dependencies.
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

These are catalog relationships, not a Maven dependency tree. There is no
`dependsOn` edge because this service has no external runtime dependencies;
JUnit is only a test dependency. Registering the API does not start the service.
