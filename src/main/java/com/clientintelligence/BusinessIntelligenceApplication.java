package com.clientintelligence;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.List;
import java.util.Map;

@SpringBootApplication
public class BusinessIntelligenceApplication {
    public static void main(String[] args) {
        SpringApplication.run(BusinessIntelligenceApplication.class, args);
    }
}

@RestController
class AnalystController {
    private static final String GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions";
    private static final String MODEL = System.getenv().getOrDefault(
        "GROQ_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct");
    private final ObjectMapper mapper = new ObjectMapper();
    private final HttpClient http = HttpClient.newBuilder()
        .connectTimeout(Duration.ofSeconds(12)).build();

    @GetMapping("/api/health")
    Map<String, Object> health(@RequestParam(defaultValue = "false") boolean deep) {
        String apiKey = System.getenv("GROQ_API_KEY");
        boolean configured = apiKey != null && !apiKey.isBlank();
        if (!deep) {
            return Map.of("status", "ok", "llmConfigured", configured,
                "llmStatus", configured ? "configured" : "not_configured", "model", MODEL);
        }
        if (!configured) {
            return Map.of("status", "ok", "llmConfigured", false,
                "llmStatus", "not_configured",
                "message", "GROQ_API_KEY is missing from the Render service environment.");
        }
        try {
            Map<String, Object> payload = Map.of(
                "model", MODEL,
                "temperature", 0,
                "max_tokens", 8,
                "messages", List.of(
                    Map.of("role", "system", "content", "Reply with the single word OK."),
                    Map.of("role", "user", "content", "Connection test.")
                )
            );
            HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(GROQ_ENDPOINT))
                .timeout(Duration.ofSeconds(18))
                .header("Authorization", "Bearer " + apiKey)
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(mapper.writeValueAsString(payload)))
                .build();
            HttpResponse<String> response = http.send(request, HttpResponse.BodyHandlers.ofString());
            if (response.statusCode() >= 200 && response.statusCode() < 300) {
                JsonNode json = mapper.readTree(response.body());
                String answer = json.path("choices").path(0).path("message").path("content").asText("");
                if (!answer.isBlank()) {
                    return Map.of("status", "ok", "llmConfigured", true,
                        "llmStatus", "connected", "model", MODEL);
                }
                return Map.of("status", "ok", "llmConfigured", true,
                    "llmStatus", "error", "model", MODEL,
                    "message", "The provider returned an empty response.");
            }
            String providerMessage = mapper.readTree(response.body()).path("error").path("message")
                .asText("Provider request failed with HTTP " + response.statusCode());
            return Map.of("status", "ok", "llmConfigured", true,
                "llmStatus", "error", "model", MODEL,
                "message", safeError(providerMessage));
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return Map.of("status", "ok", "llmConfigured", true,
                "llmStatus", "error", "model", MODEL,
                "message", "The connection test was interrupted.");
        } catch (Exception e) {
            return Map.of("status", "ok", "llmConfigured", true,
                "llmStatus", "error", "model", MODEL,
                "message", "Connection test failed. Check Render logs and the configured model.");
        }
    }

    @PostMapping("/api/chat")
    Map<String, Object> chat(@RequestBody Map<String, Object> body) {
        String question = String.valueOf(body.getOrDefault("question", "")).trim();
        String context = String.valueOf(body.getOrDefault("context", "")).trim();
        if (question.isBlank() || question.length() > 1500) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST,
                "Enter a question up to 1,500 characters.");
        }
        if (context.length() > 7000) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST,
                "Portfolio context is too large.");
        }
        String apiKey = System.getenv("GROQ_API_KEY");
        if (apiKey == null || apiKey.isBlank()) {
            throw new ResponseStatusException(HttpStatus.SERVICE_UNAVAILABLE,
                "The AI analyst is not configured yet. Add GROQ_API_KEY to the hosting provider's environment variables.");
        }
        try {
            String system = """
                You are an evidence-aware analyst for an independent client-intelligence portfolio demo.
                The dataset is entirely synthetic. Never imply that it represents real clients, a real bank,
                or confidential information. Be concise, practical, and structured. Distinguish predictive
                propensity from causal uplift; distinguish a simulated wallet-gap proxy from actual wallet
                share. Do not recommend contacting or treating any real person. Frame actions as hypotheses
                for qualified human review. State material evidence gaps and validation requirements.
                If asked for unsupported calculations, explain the limitation rather than inventing a result.
                """;
            Map<String, Object> payload = Map.of(
                "model", MODEL,
                "temperature", 0.35,
                "max_tokens", 700,
                "messages", List.of(
                    Map.of("role", "system", "content", system),
                    Map.of("role", "user", "content",
                        "Question:\n" + question + "\n\nSynthetic aggregate context (no client-level rows):\n" +
                        (context.isBlank() ? "No additional context provided." : context))
                )
            );
            String requestBody = mapper.writeValueAsString(payload);
            HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(GROQ_ENDPOINT))
                .timeout(Duration.ofSeconds(45))
                .header("Authorization", "Bearer " + apiKey)
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(requestBody))
                .build();
            HttpResponse<String> response = http.send(request, HttpResponse.BodyHandlers.ofString());
            JsonNode json = mapper.readTree(response.body());
            if (response.statusCode() < 200 || response.statusCode() >= 300) {
                String detail = json.path("error").path("message").asText("The LLM provider returned an error.");
                throw new ResponseStatusException(HttpStatus.BAD_GATEWAY, safeError(detail));
            }
            String answer = json.path("choices").path(0).path("message").path("content").asText("");
            if (answer.isBlank()) {
                throw new ResponseStatusException(HttpStatus.BAD_GATEWAY, "The model returned an empty response.");
            }
            return Map.of("answer", answer, "model", MODEL);
        } catch (ResponseStatusException e) {
            throw e;
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new ResponseStatusException(HttpStatus.GATEWAY_TIMEOUT, "The AI request was interrupted.");
        } catch (Exception e) {
            throw new ResponseStatusException(HttpStatus.BAD_GATEWAY,
                "The AI request failed. Check the deployment logs and configured model.");
        }
    }

    private String safeError(String message) {
        if (message == null || message.isBlank()) return "The LLM provider returned an error.";
        return message.length() > 240 ? message.substring(0, 240) : message;
    }
}