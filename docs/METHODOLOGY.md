# Methodology

The app creates a reproducible fictional portfolio using seeded random draws. Features include sector, region, revenue, tenure, products held, digital activity, engagement and leverage proxy. A logistic regression estimates adoption propensity using a holdout split for illustrative ROC-AUC and average precision. K-means creates four descriptive clusters. A transparent review score combines propensity, normalized simulated wallet gap and engagement.

The data-generating process is intentionally simple and known. Metrics are therefore a teaching demonstration, not evidence of real-world predictive performance. The treatment assignment and simulated outcome fields illustrate experimental thinking but should not be interpreted as a validated uplift model.
