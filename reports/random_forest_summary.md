# Random Forest Regression Summary

## Objective

The objective of this task was to train a Random Forest Regression model to predict mushroom yield using environmental sensor data and compare its performance with the previously developed Linear Regression model.

## Data Preparation

The dataset was first cleaned and feature engineered. A chronological train-test split was used to prevent data leakage, with the model trained only on historical observations and evaluated on unseen future data.

## Model Training

A Random Forest Regressor with 100 decision trees was trained using the training dataset. The model was saved to:

`models/random_forest.joblib`

## Evaluation Metrics

Model performance was evaluated on the test dataset using the following metrics:

* Mean Absolute Error (MAE)
* Root Mean Squared Error (RMSE)
* R² Score

The results were saved in:

`reports/random_forest_metrics.json`

A comparison with the Linear Regression model was generated and stored in:

`reports/model_comparison.csv`

## Feature Importance Analysis

Random Forest provides feature importance scores that indicate how much each feature contributes to the prediction. The feature importance chart was saved as:

`reports/figures/rf_importance.png`

Features with higher importance values have a stronger influence on yield prediction.

## Comparison with Linear Regression

Linear Regression assumes a linear relationship between input variables and yield, while Random Forest can model complex nonlinear relationships and interactions among features.

If the Random Forest model achieves:

* Lower MAE and RMSE
* Higher R² score

then it provides better predictive performance and its additional complexity is justified.

If the improvement is small, Linear Regression may still be preferred because it is easier to interpret and requires fewer computational resources.

## Conclusion

The Random Forest model was successfully trained, evaluated, and saved. Feature importance analysis was performed, and the model was compared against Linear Regression. The final model choice should be based on the test-set metrics and the trade-off between predictive accuracy and model interpretability.
