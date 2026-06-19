# Linear Regression Diagnostics

## Residual Calculation

Residuals were calculated as:

Residual = Actual Yield - Predicted Yield

A positive residual indicates the model under-predicted yield, while a negative residual indicates over-prediction.

## Diagnostic Figures

### Figure 1: Residuals vs Predicted Yield
File: reports/figures/residuals_linear.png

This plot checks whether residuals are randomly distributed around zero. A random scatter suggests the linear model assumptions are reasonably satisfied.

### Figure 2: Residuals vs Humidity
File: reports/figures/residuals_vs_humidity_linear.png

This plot checks whether prediction errors are related to humidity. Any visible trend may indicate that humidity has a nonlinear relationship with yield that is not fully captured by Linear Regression.

## Findings

1. Residuals are centered around zero, indicating limited overall prediction bias.
2. Some spread in residual values is visible across prediction levels, suggesting prediction uncertainty increases for certain observations.
3. Minor patterns in residuals suggest environmental variables may interact in a nonlinear manner.

## Recommendation

Linear Regression provides a useful and interpretable baseline model. However, residual patterns indicate that the relationship between temperature, humidity, CO₂, and yield may not be entirely linear.

The recommended next step is to evaluate a nonlinear model such as Random Forest Regression and compare MAE, RMSE, and R² against the linear baseline.

## Figures Referenced

- reports/figures/residuals_linear.png
- reports/figures/residuals_vs_humidity_linear.png