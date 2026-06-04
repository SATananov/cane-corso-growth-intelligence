# Classification Exercise Alignment Summary

## Classification question

The project uses a binary educational target: whether a growth interval belongs to a faster-growth period. The target is derived from interval-level weight gain per month and is used only to demonstrate a classification workflow.

## Experimental protocol

- Fixed random seed: `42`
- Main metric: `f1`
- Secondary metrics: `accuracy, precision, recall`
- Holdout test size: `0.25`
- Cross-validation: stratified folds based on available class counts
- Baselines: most-frequent dummy classifier and stratified dummy classifier

## Dataset summary

- Source rows: `32`
- Interval rows used for classification: `28`
- Training rows: `21`
- Test rows: `7`
- Positive class count: `14`
- Negative class count: `14`

## Best model in this run

The best test F1 score in this run was produced by `logistic_regression`.

The result is useful as a course-aligned classification demonstration. It should not be interpreted as a veterinary judgment or as proof that a dog is growing correctly.

## Output files

- `reports/course_exercises/classification_exercise_alignment_metrics.csv`
- `reports/course_exercises/classification_exercise_confusion_matrix.csv`
- `reports/course_exercises/classification_exercise_error_analysis.csv`
- `reports/course_exercises/classification_exercise_feature_importance.csv`
- `reports/course_exercises/classification_exercise_ablation_study.csv`
- `reports/course_exercises/classification_exercise_learning_curve.csv`
