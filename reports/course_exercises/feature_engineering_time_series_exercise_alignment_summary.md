# Feature Engineering and Time Series Exercise Alignment Summary

The workflow adapts the course exercise to longitudinal Cane Corso growth data.
The target is `weight_kg`, and the time axis is represented by age-based measurement order.

## Time audit
Dogs inspected: 4
Duplicate age measurements detected: False

## Best validation experiment
Experiment: `time_velocity_category`
Estimator: `ridge`
Feature group: time, velocity and categorical descriptors
Validation MAE: 0.570
Validation RMSE: 0.691

## Selected final test result
Estimator: `ridge`
Feature group: time, velocity and categorical descriptors
Test MAE: 0.552
Test RMSE: 0.700
Test R²: 0.969

## Interpretation boundary
The dataset is small and educational. The result demonstrates a leakage-aware feature-engineering and time-series modelling workflow, not a production biological growth forecast.
