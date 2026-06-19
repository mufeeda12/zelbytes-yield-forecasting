# Cross Validation Results

## Method
TimeSeriesSplit with 5 folds was used to preserve chronological order and prevent data leakage.

## Linear Regression
- Fold MAE: [0.08258477698934343, 0.07396206691929362, 0.08483220289663401, 0.07417082185768414, 0.0783616869731276]
- Average CV MAE: 0.0788
- Standard Deviation: 0.0044

## Random Forest
- Fold MAE: [0.0827967213114752, 0.05508524590163937, 0.06568032786885258, 0.05377540983606568, 0.0585360655737706]
- Average CV MAE: 0.0632
- Standard Deviation: 0.0106

## Overfitting Analysis
Linear Regression train MAE = 0.0780, test MAE = 0.0838. The small difference suggests limited overfitting and good generalization.

## Variance Interpretation
A low standard deviation indicates stable model performance across folds. A high standard deviation suggests the model performance varies between time periods.

## Conclusion
Random Forest achieved a lower average CV MAE and therefore performed better during cross-validation.