-- Example SQL transformation for a client intelligence mart.
SELECT client_id, sector, region, annual_revenue_usd_m,
       relationship_tenure_years, products_held,
       digital_activity_score, engagement_score,
       estimated_wallet_gap_usd_m,
       CASE WHEN digital_activity_score >= 0.65 AND engagement_score >= 0.60
            THEN 'Engaged digital relationship'
            WHEN products_held <= 2 THEN 'Potential product breadth review'
            ELSE 'Relationship context review' END AS review_hypothesis
FROM synthetic_client_snapshot;
