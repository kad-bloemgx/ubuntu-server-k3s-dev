package nl.kadaster.demo;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;

public final class DemoApplication {
    private DemoApplication() {}

    public static void main(String[] args) throws IOException {
        if (args.length > 1) {
            throw new IllegalArgumentException("Usage: java -jar java-demo.jar [port]");
        }
        int port = args.length == 0 ? 8080 : Integer.parseInt(args[0]);
        if (port < 1 || port > 65535) {
            throw new IllegalArgumentException("Port must be between 1 and 65535");
        }
        HttpServer server = start(port);
        Runtime.getRuntime().addShutdownHook(new Thread(() -> server.stop(0)));
        System.out.println("Java demo listening at http://127.0.0.1:" + port + "/api/greeting");
    }

    static HttpServer start(int port) throws IOException {
        HttpServer server = HttpServer.create(new InetSocketAddress("127.0.0.1", port), 0);
        server.createContext("/", DemoApplication::handle);
        server.start();
        return server;
    }

    private static void handle(HttpExchange exchange) throws IOException {
        try (exchange) {
            int status;
            String body;
            if (!"/api/greeting".equals(exchange.getRequestURI().getPath())) {
                status = 404;
                body = "{\"error\":\"Not found\"}";
            } else if (!"GET".equals(exchange.getRequestMethod())) {
                status = 405;
                exchange.getResponseHeaders().set("Allow", "GET");
                body = "{\"error\":\"Method not allowed\"}";
            } else {
                status = 200;
                body = "{\"message\":\"Hello from Java demo\"}";
            }
            byte[] bytes = body.getBytes(StandardCharsets.UTF_8);
            exchange.getResponseHeaders().set("Content-Type", "application/json; charset=utf-8");
            if ("HEAD".equals(exchange.getRequestMethod())) {
                exchange.sendResponseHeaders(status, -1);
            } else {
                exchange.sendResponseHeaders(status, bytes.length);
                exchange.getResponseBody().write(bytes);
            }
        }
    }
}
