# Vanguard CX Analytics Team Project

## Project Overview

This repository contains the work for the **Vanguard A/B Test** project, conducted by [Your Name 1] and [Your Name 2]. The project focuses on analyzing the results of an A/B test conducted by Vanguard, a leading investment management company. The goal is to assess the impact of a new user interface (UI) design on client experience and process completion rates.

The primary objective of the project is to perform exploratory data analysis (EDA), hypothesis testing, and experiment evaluation to determine if the redesigned UI leads to improved client outcomes.


## Table of Contents
- [Project Overview](#project-overview)
- [Data Overview](#data-overview)
- [Methodology](#methodology)
- [Deliverables](#deliverables)
- [Team Members](#team-members)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)


## Data Overview

The project uses the following datasets:
1. **Client Profiles (df_final_demo)** - Contains demographic information such as age, gender, and account details of clients.
2. **Digital Footprints (df_final_web_data)** - Tracks detailed client interactions online, split into two parts (pt_1 and pt_2).
3. **Experiment Roster (df_final_experiment_clients)** - Contains the list of clients who participated in the A/B test, with information about which group (Control vs. Test) they were assigned to.

The datasets need to be merged and cleaned before performing any analysis.


## Methodology

### 1. **Exploratory Data Analysis (EDA) and Data Cleaning**
   - Initial data exploration using Python libraries such as **Pandas**, **Matplotlib**, and **Seaborn**.
   - Data cleaning to address missing values, outliers, and inconsistencies.

### 2. **Performance Metrics**
   - Definition and calculation of key performance indicators (KPIs) like completion rates, time spent on each step, and error rates.

### 3. **Hypothesis Testing**
   - A/B test analysis to compare the completion rates between the Control and Test groups.
   - Additional hypothesis tests to assess factors like age, gender, and client tenure.
   - Statistical tests (e.g., Two-proportion Z-test) to evaluate significance.

### 4. **Experiment Evaluation**
   - Assessment of the experiment design, including randomization, potential biases, and the experiment duration.
   - Suggestions for additional data that could enhance the analysis.

### 5. **Visualization**
   - **Tableau**: Creation of interactive visualizations to provide insights into the experiment data.
   - **Streamlit**: (Optional) Build interactive web apps for real-time analysis and visualization.


## Deliverables

- A detailed analysis report, including findings, conclusions, and recommendations for Vanguard.
- A Tableau dashboard visualizing key insights.
- Jupyter notebooks with code for EDA, hypothesis testing, and experiment evaluation.
- A well-documented README with explanations of methodology, results, and conclusions.
- A project presentation summarizing the findings and insights.


## The Team
- Constanza
- Bru
