# W01 Physical AI Data Landscape

## 1. Problem Statement

This week focuses on understanding InGen Dynamics' physical AI and robotics platforms from a data analyst perspective. The main goal is to identify what types of data each platform may generate, what operational questions can be answered with data analysis, and what variables could be used for future regression, classification, and KPI analysis.

## 2. InGen Platform Data Map

### 2.1 Aido Rover

- Operational question:Which sensor and operational variables are most strongly associated with Aido Rover fault risk during outdoor patrol and inspection tasks?
- Data type:Robot telemetry data, including GPS location, LiDAR distance, battery state of charge, wheel torque values, ambient temperature, operating hours, deployment zone, and fault labels.
- Response variable:Fault status or fault probability. This can be represented as a binary variable where 0 = normal operation and 1 = fault.
- Candidate predictor variables:Battery state of charge, LiDAR distance variance, wheel torque variance, ambient temperature, operating hours, deployment zone, firmware version, and patrol distance.

### 2.2 Sentinel Prime AI

- Operational question:Which zones, event types, or severity patterns indicate higher security risk?
- Data type:Security event logs, sensor alerts, timestamps, location zones, event types, and severity levels.
- Response variable:Event severity, alert frequency, or high-risk zone classification.
- Candidate predictor variables:Location zone, time of day, event type, sensor type, historical event count, and recent alert frequency.

### 2.3 Fari

- Operational question:Which interaction features are associated with higher user engagement or interaction quality for eldercare support?
- Data type:Interaction logs, session duration, response length, sentiment score, latency, topic coherence, and user engagement indicators.
- Response variable:Interaction quality or user engagement level.
- Candidate predictor variables:Session duration, response length, sentiment score, latency, topic coherence, and number of completed interactions.

### 2.4 Senpai

- Operational question:Which learning interaction patterns are associated with student progress and engagement?
- Data type:Learning session data, quiz results, completion rates, interaction frequency, response accuracy, and time spent on activities.
- Response variable:Learning progress, engagement score, or task completion rate.
- Candidate predictor variables:Session duration, number of completed tasks, quiz accuracy, response time, interaction frequency, and topic difficulty.

### 2.5 Aido Humanoid

- Operational question:Which movement or sensor patterns define different operational modes such as walking, reaching, and idle behavior?
- Data type:Joint sensor data, movement velocity, balance signals, battery status, task type, and operating mode labels.
- Response variable:Operational mode or movement classification.
- Candidate predictor variables:Joint velocity, acceleration, balance signal, task type, battery state, and sensor variance.

## 3. Origami AI / PIC 2.0 Data Map

## 4. Reference Summaries

### Reference 1: InGen product and platform materials

Most important concept:InGen Dynamics positions its products as part of a connected physical AI ecosystem, where robotics platforms such as Aido Rover, Sentinel Prime AI, Fari, Senpai, and Aido Humanoid generate operational data that can be analyzed to improve performance, safety, interaction quality, and deployment decisions.

How it applies to InGen data analysis:This concept helps frame each product as a data-generating platform. Instead of only describing the robots, a data analyst should ask what variables each platform produces, what outcome should be predicted, and what metrics can support operational decisions.

### Reference 2: Sensor data analysis for mobile robot fleets

Most important concept:Mobile robot fleets can be monitored through telemetry data such as battery state of charge, GPS position, LiDAR distance, wheel torque, temperature, and fault events.

How it applies to InGen data analysis:This directly supports the Aido Rover analysis. These telemetry variables can be used as candidate predictors in regression or classification models to identify which sensor patterns are most strongly associated with fault risk.

### Reference 3: Exploratory data analysis best practices

Most important concept:Exploratory data analysis should begin with a clear problem statement, followed by data structure inspection, missing value checks, distribution analysis, outlier detection, and visual comparison between key groups.

How it applies to InGen data analysis:For the synthetic Aido Rover dataset, EDA will help identify whether normal and fault cases show different patterns in battery level, LiDAR readings, wheel torque, or temperature. These early visual findings will guide later correlation and regression analysis.

### Reference 4: Multivariate regression methodology

Most important concept:Multivariate regression is used to estimate how multiple predictor variables are associated with an outcome variable while controlling for other variables in the model.

How it applies to InGen data analysis:This connects directly to my previous Tsinghua research on Shanghai rental prices. In that project, regression was used to identify key determinants of rental price. In this internship, the same methodology can be applied to identify key determinants of Aido Rover fault probability.

### Reference 5: SQL for data analytics

Most important concept:SQL allows analysts to query structured operational data directly through filtering, aggregation, joins, common table expressions, and window functions.

How it applies to InGen data analysis:For robot fleet analytics, SQL can be used to calculate fault rates by unit, compare deployment zones, identify high-risk robots, summarize Sentinel event logs, and build repeatable KPI reporting pipelines.

## 5. Initial Analytical Insights

## 6. Next Steps