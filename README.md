# Business Intelligence — Client Intelligence Lab

An independent portfolio project demonstrating a corporate and institutional banking client-intelligence workflow with a polished HTML/CSS/JavaScript interface and a Java Spring Boot backend for secure Groq LLM calls.

> **Synthetic-data disclaimer:** This project is independent and is not affiliated with HSBC. All client records, outcomes, metrics and opportunity proxies are fictional. It does not use HSBC systems or confidential data.

## Technology

- **Frontend:** semantic HTML, responsive CSS, vanilla JavaScript, SVG charts
- **Backend:** Java 21, Spring Boot, REST API
- **LLM:** Groq Chat Completions API; configurable with `GROQ_MODEL`
- **Hosting:** Docker / Render blueprint
- **Analytics:** browser-generated synthetic portfolio, propensity proxy, transparent review heuristic, sector summaries, CSV exports

## Run locally

Install Java 21 and Maven. In a terminal, set the Groq key as an environment variable (never paste it into JavaScript or commit it):

```bash
export GROQ_API_KEY="your-new-rotated-key"
# Optional:
export GROQ_MODEL="meta-llama/llama-4-scout-17b-16e-instruct"
mvn spring-boot:run
```

Open http://localhost:8080. The dashboard itself works without a Groq key; the AI analyst requires a valid key and an available model on your Groq account. On Windows PowerShell, use `$env:GROQ_API_KEY="your-new-rotated-key"`.

## Deploy

1. Open [Render](https://render.com/) and connect your GitHub account.
2. Create a **Blueprint** from this repository, or create a web service using its Dockerfile.
3. Set `GROQ_API_KEY` in the Render service's **Environment** settings using a newly rotated key. Never add the value to GitHub.
4. Keep `GROQ_MODEL` set to a model enabled for your Groq account.
5. Deploy. The service exposes `/api/health` for health checks and `/api/chat` for the LLM proxy.

Blueprint: [render.yaml](render.yaml). Deployment notes: [DEPLOY_JAVA_RENDER.md](DEPLOY_JAVA_RENDER.md).

## Dashboard features

- **Portfolio overview:** synthetic portfolio KPIs, sector mix, propensity versus simulated wallet-gap proxy.
- **Client explorer:** search and filter synthetic records; inspect a fictional relationship profile; export CSV.
- **RM action queue:** transparent review prioritisation and review prompts; export the queue.
- **Evidence & model review:** visible validation checks, methodology, limitations, and production requirements.
- **AI analyst:** Groq LLM answers questions using aggregate synthetic metrics only. The API key stays server-side.

## Method and limitations

- Adoption propensity is a **predictive synthetic score**, not causal uplift.
- The wallet-gap value is a simulated proxy, not actual bank wallet share or a forecast.
- Review priority is a transparent heuristic, not a credit, suitability, pricing, or client-treatment decision.
- The browser generates fictional records; the AI proxy receives only aggregate statistics, not individual client rows.
- LLM outputs are unverified drafts and require human review.
- Production use would require approved data access, privacy/security controls, independent validation, monitoring, fairness review, business sign-off, and accountable human ownership.

## Repository layout

- `src/main/resources/static/index.html` — complete responsive frontend.
- `src/main/java/com/clientintelligence/BusinessIntelligenceApplication.java` — Spring Boot server and Groq proxy.
- `pom.xml` — Java dependencies.
- `Dockerfile`, `render.yaml` — container and hosting configuration.
- `sql/` — illustrative SQL schema, client-intelligence mart and review queue.
- `docs/` — methodology, governance, business case and agentic analytics notes.
- `app.py` — legacy Streamlit version retained for reference; the new default experience is Java + HTML/CSS/JavaScript.

## Secret safety

A Groq key was pasted into a chat and should be treated as exposed. **Revoke it in Groq immediately and create a replacement.** Only store the replacement in local environment variables or the hosting provider's secret/environment settings. Do not commit secrets or put them in frontend JavaScript.
