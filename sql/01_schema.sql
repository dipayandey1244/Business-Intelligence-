-- Illustrative SQL schema; all fields are synthetic.
CREATE TABLE synthetic_client_snapshot (
  client_id VARCHAR(32) PRIMARY KEY,
  sector VARCHAR(64),
  region VARCHAR(64),
  annual_revenue_usd_m DECIMAL(14,2),
  relationship_tenure_years INTEGER,
  products_held INTEGER,
  digital_activity_score DECIMAL(6,3),
  engagement_score DECIMAL(6,3),
  leverage_proxy DECIMAL(6,3),
  adopted_simulated INTEGER,
  estimated_wallet_gap_usd_m DECIMAL(14,2)
);
