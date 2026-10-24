-- Human-review queue only; never triggers client contact.
SELECT client_id, sector, region, adoption_propensity,
       estimated_wallet_gap_usd_m, review_priority_score, priority_band,
       'Human review required; validate need, eligibility and suitability' AS guardrail
FROM scored_synthetic_clients
WHERE evidence_checks_passed = TRUE
ORDER BY review_priority_score DESC;
