# Week 3 Data Analyst Log

## What I Analyzed

This week, I performed correlation analysis and multivariate OLS regression on the synthetic Aido Rover telemetry dataset. The main goal was to identify which sensor variables are the strongest determinants of Aido Rover fault status. This analysis built on the Week 1 exploratory data analysis and the Week 2 SQL analysis.

## What I Found

The correlation analysis showed that wheel torque variables, battery state of charge, and LiDAR distance had the strongest relationships with `fault_label`. The four wheel torque variables were highly correlated with each other, so I created an engineered feature called `torque_mean` to reduce multicollinearity.

The final selected regression model used three predictors: `torque_mean`, `battery_soc`, and `lidar_dist`. The model achieved an R-squared value of approximately 0.55056, which was almost the same as the full model that used all original sensor variables.

## Key Insight

The most important finding was that a simpler engineered model can explain almost the same amount of variation as the full sensor model. `torque_mean` was the strongest positive determinant of fault status, followed by `battery_soc` as the strongest negative determinant and `lidar_dist` as another positive determinant.

## Model Limitation

The residual diagnostic plots showed that OLS has limitations because `fault_label` is a binary outcome. The residuals were not normally distributed, and the scale-location plot suggested non-constant variance. Therefore, the OLS model should be interpreted as a linear probability model rather than a final classification model.

## Next Step

The Week 3 results will support Week 4 logistic regression. Since `fault_label` is binary, logistic regression will be more appropriate for fault classification. The Week 4 model should use `torque_mean`, `battery_soc`, and `lidar_dist` as starting predictors and evaluate model performance using classification metrics such as accuracy, precision, recall, F1-score, confusion matrix, and ROC-AUC.