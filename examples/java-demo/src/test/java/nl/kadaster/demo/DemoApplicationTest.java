package nl.kadaster.demo;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.sun.net.httpserver.HttpServer;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class DemoApplicationTest {
    private HttpServer server;
    private String baseUrl;
    private final HttpClient client = HttpClient.newHttpClient();

    @BeforeEach
    void start() throws Exception {
        server = DemoApplication.start(0);
        baseUrl = "http://127.0.0.1:" + server.getAddress().getPort();
    }

    @AfterEach
    void stop() {
        server.stop(0);
    }

    @Test
    void servesGreeting() throws Exception {
        var response = request("/api/greeting", "GET");
        assertEquals(200, response.statusCode());
        assertEquals("{\"message\":\"Hello from Java demo\"}", response.body());
        assertEquals("application/json; charset=utf-8",
                response.headers().firstValue("Content-Type").orElseThrow());
    }

    @Test
    void rejectsUnknownPathsAndPrefixMatches() throws Exception {
        for (String path : new String[] {"/", "/missing", "/api/greeting/extra"}) {
            var response = request(path, "GET");
            assertEquals(404, response.statusCode());
            assertEquals("{\"error\":\"Not found\"}", response.body());
        }
    }

    @Test
    void rejectsUnsupportedMethods() throws Exception {
        var response = request("/api/greeting", "POST");
        assertEquals(405, response.statusCode());
        assertEquals("GET", response.headers().firstValue("Allow").orElseThrow());
        assertEquals("{\"error\":\"Method not allowed\"}", response.body());
    }

    @Test
    void rejectsHeadWithoutResponseBody() throws Exception {
        var response = request("/api/greeting", "HEAD");
        assertEquals(405, response.statusCode());
        assertEquals("", response.body());
        assertEquals("GET", response.headers().firstValue("Allow").orElseThrow());
    }

    private HttpResponse<String> request(String path, String method) throws Exception {
        return client.send(HttpRequest.newBuilder(URI.create(baseUrl + path))
                        .timeout(Duration.ofSeconds(5))
                        .method(method, HttpRequest.BodyPublishers.noBody())
                        .build(),
                HttpResponse.BodyHandlers.ofString());
    }
}
