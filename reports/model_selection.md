# Model Comparison and Champion Selection

## Comparison Summary

Three models were evaluated on the same untouched test dataset:

1. Linear Regression
2. Random Forest (Default)
3. Tuned Random Forest

The comparison metrics include MAE, RMSE, and R² score. Results are available in:

`reports/model_comparison.csv`

## Champion Model

Champion Model: Tuned Random Forest

The tuned Random Forest achieved the best overall predictive performance on the test set, producing the lowest prediction error and highest R² score. Hyperparameter tuning improved the model's ability to capture nonlinear relationships between environmental variables and mushroom yield.

## Agritech Considerations

Underestimating yield may result in insufficient labor allocation and missed harvesting opportunities.

Overestimating yield may lead to unmet buyer expectations, delivery shortfalls, and planning inefficiencies.

Because of these operational impacts, minimizing prediction error is important for production planning.

## Visualization

The predicted versus actual yield plot for the champion model was saved as:

`reports/figures/pred_vs_actual.png`

Points closer to the diagonal reference line indicate more accurate predictions.

## Limitations

* The model is trained only on the available sensor ranges present in the dataset.
* Predictions may be less reliable when environmental conditions fall outside the observed training range.
* Seasonal effects and long-term environmental changes may not be fully captured.
* The model should be used as a decision-support tool rather than a replacement for grower expertise.

## Conclusion

The Tuned Random Forest was selected as the final model because it achieved the best balance of predictive accuracy and generalization performance on the test dataset.
