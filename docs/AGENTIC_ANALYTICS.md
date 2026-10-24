# AI-assisted analytics and agent boundaries

The AI analyst is an optional drafting assistant, not an autonomous decision-maker. It receives only aggregate synthetic metrics in this demo.

## Suggested agent responsibilities
1. **Planner:** restate the business question, define scope, and list assumptions.
2. **Analyst:** interpret the supplied aggregates without inventing metrics.
3. **Model reviewer:** distinguish prediction from causality and identify validation gaps.
4. **Recommendation writer:** propose hypotheses and human-review steps, not client instructions.
5. **Evidence gate:** deterministic data and policy checks remain authoritative outside the LLM.

## Controls
- Keep API keys in Streamlit Secrets or environment variables.
- Never send client-level or confidential data to an external LLM without explicit institutional approval.
- Treat generated content as unverified. Reconcile figures against the dashboard and source data.
- Do not use generated text to automate client contact, credit, pricing, eligibility, or suitability decisions.
- Log prompts, outputs, versions, reviewer actions, and exceptions in a production design with approved controls.

## Known limitations
The demo is not a full production multi-agent orchestration platform, does not have institutional identity/access controls, and does not demonstrate an approved bank data connection. LLM availability and output quality depend on provider/model changes.
