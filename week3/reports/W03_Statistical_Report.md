# W03 Statistical Report

## Problem Statement

This report analyzes the strongest statistical determinants of Aido Rover fault status using the synthetic rover telemetry dataset. The main research question is:

**Which sensor variables are the strongest determinants of Aido Rover fault probability?**

This Week 3 analysis builds on the Week 1 exploratory data analysis and the Week 2 SQL fleet analysis. Week 1 and Week 2 showed that fault rows tend to have lower battery state of charge, higher LiDAR distance values, and higher wheel torque values. This report tests those relationships more formally through correlation analysis and multivariate OLS regression.

Because the dependent variable `fault_label` is binary, the OLS regression model should be interpreted as a linear probability model. The goal of this week is not to create the final classification model, but to identify statistically significant fault determinants before moving into logistic regression in Week 4.

---

## Data Source

The analysis uses the synthetic Aido Rover telemetry dataset generated in Week 1. The dataset contains 15,000 telemetry records and includes the following variables:

| Variable | Description |
|---|---|
| `gps_lat` | Simulated GPS latitude |
| `gps_lon` | Simulated GPS longitude |
| `lidar_dist` | Simulated LiDAR distance reading |
| `battery_soc` | Battery state of charge |
| `torque_fl` | Front-left wheel torque |
| `torque_fr` | Front-right wheel torque |
| `torque_rl` | Rear-left wheel torque |
| `torque_rr` | Rear-right wheel torque |
| `ambient_temp` | Ambient temperature |
| `fault_label` | Binary fault label, where 0 = normal and 1 = fault |

All data used in this analysis is synthetic. It does not contain confidential company data, customer data, internal product data, or proprietary system logs.

---

## Correlation Analysis

The first step was to calculate the Pearson correlation between each numeric sensor variable and `fault_label`.

The strongest correlations with `fault_label` were:

| Variable | Correlation with Fault Label | Direction |
|---|---:|---|
| `torque_fr` | approximately 0.57 | Positive |
| `torque_fl` | approximately 0.56 | Positive |
| `torque_rl` | approximately 0.56 | Positive |
| `torque_rr` | approximately 0.56 | Positive |
| `battery_soc` | approximately -0.56 | Negative |
| `lidar_dist` | approximately 0.45 | Positive |

The results show that wheel torque variables are positively associated with fault status. This means higher wheel torque values are associated with a higher probability of fault. Battery state of charge is negatively associated with fault status, meaning lower battery levels are associated with higher fault probability. LiDAR distance is also positively associated with fault status.

GPS latitude, GPS longitude, and ambient temperature showed very weak relationships with fault status. Therefore, they were not selected as major candidate predictors.

---

## Candidate Predictor Selection

A variable was selected as a candidate predictor if it met both of the following conditions:

- Absolute Pearson correlation greater than 0.10
- p-value less than 0.05

The selected candidate predictors were:

| Candidate Predictor |
|---|
| `torque_fr` |
| `torque_rl` |
| `torque_rr` |
| `torque_fl` |
| `battery_soc` |
| `lidar_dist` |

These candidate predictors are consistent with the Week 2 SQL findings. The SQL comparison between normal rows and fault rows showed that fault rows had lower battery state of charge, higher LiDAR distance, and higher wheel torque values.

---

## Multicollinearity Check

The correlation matrix showed strong multicollinearity among the four wheel torque variables.

| Feature 1 | Feature 2 | Correlation |
|---|---|---:|
| `torque_fl` | `torque_fr` | 0.895487 |
| `torque_fl` | `torque_rl` | 0.895557 |
| `torque_fl` | `torque_rr` | 0.896542 |
| `torque_fr` | `torque_rl` | 0.894264 |
| `torque_fr` | `torque_rr` | 0.896544 |
| `torque_rl` | `torque_rr` | 0.895435 |

All four torque variables were highly correlated with one another, with correlations around 0.89 to 0.90. Including all four torque variables in the final model could make the regression coefficients unstable and harder to interpret.

To reduce multicollinearity, the four torque variables were combined into one engineered feature:

`torque_mean`

This variable represents the average wheel torque across all four wheels.

---

## Regression Model Design

Three OLS regression models were tested.

| Model | Description |
|---|---|
| Full Original Sensor Model | Uses all original sensor variables |
| Correlation-Screened Engineered Model | Uses selected predictors after correlation screening and feature engineering |
| Final Selected Model | Uses the final statistically significant predictors |

The predictors were standardized before regression, so coefficient magnitudes can be compared directly. Larger absolute coefficient values indicate stronger determinants of fault status.

---

## Model Comparison

| Model | Number of Features | R-squared | Adjusted R-squared | F-statistic | F p-value |
|---|---:|---:|---:|---:|---:|
| Full Original Sensor Model | 9 | 0.55078 | 0.55051 | 2042.12226 | < 0.001 |
| Correlation-Screened Engineered Model | 3 | 0.55056 | 0.55047 | 6123.22571 | < 0.001 |
| Final Selected Model | 3 | 0.55056 | 0.55047 | 6123.22571 | < 0.001 |

The full model used 9 predictors and achieved an R-squared value of approximately 0.55078. The final selected model used only 3 predictors and achieved an R-squared value of approximately 0.55056.

This means the simpler final model explains almost the same amount of variation in fault status as the full model. Therefore, the final selected model is preferred because it is more interpretable and avoids unnecessary predictors.

---

## Final Selected Model

The final selected predictors were:

| Final Predictor |
|---|
| `torque_mean` |
| `battery_soc` |
| `lidar_dist` |

The regression result was:

| Variable | Coefficient | Standard Error | t-statistic | p-value |
|---|---:|---:|---:|---:|
| `const` | 0.12413 | 0.00181 | 68.76622 | < 0.001 |
| `torque_mean` | 0.13160 | 0.00195 | 67.36213 | < 0.001 |
| `battery_soc` | -0.11942 | 0.00195 | -61.31288 | < 0.001 |
| `lidar_dist` | 0.08349 | 0.00190 | 43.90997 | < 0.001 |

All three predictors are statistically significant at the p < 0.001 level.

---

## Top Determinants of Fault Status

Because all predictors were standardized, the absolute coefficient values can be used to compare the relative strength of each determinant.

| Rank | Variable | Coefficient | Absolute Coefficient | Interpretation |
|---:|---|---:|---:|---|
| 1 | `torque_mean` | 0.13160 | 0.13160 | Higher average wheel torque is associated with higher fault probability |
| 2 | `battery_soc` | -0.11942 | 0.11942 | Higher battery state of charge is associated with lower fault probability |
| 3 | `lidar_dist` | 0.08349 | 0.08349 | Higher LiDAR distance is associated with higher fault probability |

The strongest positive determinant is `torque_mean`. This suggests that higher mechanical load or movement difficulty may be associated with greater fault risk.

The strongest negative determinant is `battery_soc`. This suggests that better battery health is associated with lower fault risk.

The third strongest determinant is `lidar_dist`. Higher LiDAR distance values may reflect more difficult navigation conditions, sensor instability, or environmental complexity.

---

## Interpretation of Coefficients

The coefficient for `torque_mean` is positive. Holding other variables constant, a one-standard-deviation increase in average wheel torque is associated with an approximate 0.1316 increase in predicted fault probability.

The coefficient for `battery_soc` is negative. Holding other variables constant, a one-standard-deviation increase in battery state of charge is associated with an approximate 0.1194 decrease in predicted fault probability.

The coefficient for `lidar_dist` is positive. Holding other variables constant, a one-standard-deviation increase in LiDAR distance is associated with an approximate 0.0835 increase in predicted fault probability.

These results are consistent with the Week 2 SQL analysis. Fault rows had lower battery state of charge, higher LiDAR distance, and higher wheel torque values than normal rows.

---

## Residual Diagnostics

Three residual diagnostic plots were reviewed:

1. Residuals vs. fitted values plot
2. Q-Q plot of residuals
3. Scale-location plot

### Residuals vs. Fitted Values

The residuals vs. fitted values plot showed two clear diagonal bands. This pattern is expected because the dependent variable `fault_label` is binary and can only take values of 0 or 1. The plot suggests that OLS is not ideal as a final classification model for this task.

### Q-Q Plot

The Q-Q plot showed that the residuals deviate from the normality line. This indicates that the residuals are not normally distributed. This result is also expected because the outcome variable is binary.

### Scale-Location Plot

The scale-location plot showed a clear pattern rather than a random spread. This suggests non-constant variance, also known as heteroscedasticity. This is a common limitation when using OLS regression with a binary dependent variable.

---

## Model Limitations

The main limitation of this Week 3 model is that `fault_label` is a binary outcome. OLS regression assumes a continuous dependent variable, normally distributed residuals, and constant error variance. These assumptions are not fully satisfied in this case.

Therefore, the OLS model should be interpreted as a linear probability model. It is useful for identifying statistically significant determinants of fault risk, but it should not be treated as the final predictive classification model.

Another limitation is that the dataset is synthetic. The relationships found in this report reflect the structure of the simulated data and should not be interpreted as real-world performance results for actual Aido Rover units.

---

## Recommendation for Week 4

The Week 3 analysis identified three statistically significant determinants of Aido Rover fault status:

1. `torque_mean`
2. `battery_soc`
3. `lidar_dist`

These variables should be used as the starting predictors for Week 4 logistic regression and classification modeling. Logistic regression is more appropriate than OLS because the target variable is binary.

In Week 4, the analysis should evaluate classification performance using metrics such as:

- accuracy
- precision
- recall
- F1-score
- confusion matrix
- ROC-AUC

The Week 4 model should test whether `torque_mean`, `battery_soc`, and `lidar_dist` can accurately classify fault and normal records.

---

## Conclusion

This Week 3 statistical analysis found that average wheel torque, battery state of charge, and LiDAR distance are the strongest determinants of Aido Rover fault status in the synthetic telemetry dataset.

The final selected OLS model achieved an R-squared value of approximately 0.55056 using only three predictors. This performance was almost identical to the full model with nine predictors, showing that a simpler engineered model can explain most of the same variation while remaining easier to interpret.

The most important determinant was `torque_mean`, followed by `battery_soc` and `lidar_dist`. Higher average wheel torque and higher LiDAR distance were associated with higher fault probability, while higher battery state of charge was associated with lower fault probability.

However, residual diagnostics showed that OLS has clear limitations for this task because the target variable is binary. For this reason, the Week 3 OLS model should be treated as a determinant analysis model, not as the final fault classification model. Week 4 should extend this work using logistic regression.