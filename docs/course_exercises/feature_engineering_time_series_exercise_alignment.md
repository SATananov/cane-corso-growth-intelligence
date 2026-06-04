# Feature Engineering and Time Series Exercise Alignment

This document connects the course exercise on feature engineering and time-series modelling with the Cane Corso Growth Intelligence project.

The exercise uses a traffic-volume dataset and asks for a complete workflow around time-based data: problem formulation, time-column audit, baseline forecasting, iterative improvements, categorical features, pipelines, chronological testing, ablation, residual analysis, and a multi-horizon forecasting discussion.

The project adapts the same machine-learning process to longitudinal Cane Corso growth measurements. The target is `weight_kg`, and the time axis is represented by `age_months`. Since the prototype dataset does not contain real calendar timestamps, the project derives a synthetic `measurement_date` only for time-index audit and chronological modelling demonstrations. The modelling interpretation remains educational.

## Project translation

| Exercise idea | Project version |
|---|---|
| traffic volume target | Cane Corso weight trajectory target |
| date/time feature | age-based longitudinal measurement order |
| lag features | previous weight and previous height |
| rolling windows | rolling average weight and growth velocity |
| categorical/text-like features | sex and activity level |
| leakage-aware testing | chronological split by age within dog trajectories |
| residual analysis | errors by age group and dog |
| multi-horizon forecasting | direct and recursive future-weight forecasting plan |

## Important limitations

The current dataset is intentionally small and educational. The results show the workflow and reasoning process, not a production-grade biological growth model. A real deployment would require a larger longitudinal dataset, more dogs, repeated measurements over time, and careful validation with domain experts.
