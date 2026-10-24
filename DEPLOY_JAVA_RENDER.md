# Deploy the Java web app on Render

This repository now serves the dashboard from a Java 21 / Spring Boot application. You do not need Streamlit to run the new interface.

## Steps

1. Sign in to [Render](https://render.com/) and connect GitHub.
2. Choose **New → Blueprint** and select `dipayandey1244/Business-Intelligence-`. Render reads `render.yaml` and the `Dockerfile`.
3. When prompted, set `GROQ_API_KEY` to a **newly rotated** Groq API key in Render's environment settings. Do not commit the value to the repository.
4. Confirm `GROQ_MODEL` is available to your Groq account. The default in `render.yaml` is `meta-llama/llama-4-scout-17b-16e-instruct`; change it in Render environment settings if that model is unavailable.
5. Start the deployment and wait for the build to finish.
6. Open the Render-provided HTTPS URL. The dashboard loads at the root path; `/api/health` shows whether the server is running and whether an API key is configured.

## Local development

Requires Java 21 and Maven:

```bash
export GROQ_API_KEY="your-new-rotated-key"
mvn spring-boot:run
```

Then open http://localhost:8080. The dashboard and synthetic-data features work without an API key. The AI analyst requires the backend environment variable and a valid Groq model.

## Security notes

- A key previously pasted into a chat should be considered exposed: revoke it and replace it.
- The frontend never contains the Groq key. Calls go to the Java endpoint `POST /api/chat`.
- The endpoint forwards the question plus aggregate synthetic metrics only; it does not send individual client rows.
- For a public production service, consider rate limiting, abuse protection, usage budgets, request logging policy, and authentication if the audience is not meant to be public.
- This is an educational synthetic-data project, not affiliated with HSBC and not suitable for real client decisions.
