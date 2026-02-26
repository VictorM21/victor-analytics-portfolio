&nbsp;A/B Testing Simulation Portfolio



&nbsp;📋 Overview

This project demonstrates a complete A/B testing workflow including sample size calculation, experiment simulation, statistical analysis, and results interpretation. It showcases proficiency in experimental design, statistical methods, and data-driven decision making.



&nbsp;🎯 Key Features



&nbsp;1. Sample Size Calculator

\- Determines required sample size based on:

&nbsp; - Baseline conversion rate

&nbsp; - Minimum detectable effect

&nbsp; - Significance level (α)

&nbsp; - Statistical power (1-β)

\- Visualizes sample size trade-offs



&nbsp;2. Experiment Simulator

\- Generates realistic A/B test data

\- Controls for random variation

\- Simulates different effect sizes

\- Multiple scenario testing



&nbsp;3. Statistical Analysis

\- Hypothesis testing (Z-test, Chi-square)

\- P-value calculation

\- Confidence intervals

\- Power analysis

\- Practical significance assessment



&nbsp;4. Visualization Dashboard

\- Conversion rate bar charts

\- Effect size with confidence intervals

\- Individual conversion distributions

\- Power analysis curves

\- Sample size heatmaps



&nbsp;📁 Project Structure



07-ab-testing/

├── scripts/

│ ├── ab\_testing\_simulation.py  Main A/B testing class

│ └── sample\_size\_calculator.py  Sample size dashboard

├── data/

│ └── (generated during simulation)

├── results/

│ ├── ab\_test\_visualization.png  Experiment plots

│ ├── sample\_size\_dashboard.png  Sample size analysis

│ ├── ab\_test\_report.csv  Results export

│ └── multiple\_scenarios.csv  Scenario comparison

└── documentation/

└── README.md  This file



&nbsp;📊 Statistical Concepts Demonstrated



| Concept | Implementation |

|---------|----------------|

| Hypothesis Testing | H₀: No difference vs H₁: Treatment effect |

| P-value | Probability of observing data if H₀ is true |

| Confidence Intervals | Range of plausible effect sizes |

| Statistical Power | Probability of detecting true effect |

| Type I Error (α) | False positive rate (5%) |

| Type II Error (β) | False negative rate (20%) |

| Effect Size | Magnitude of improvement |

| Sample Size Calculation | Ensuring adequate power |



&nbsp;🚀 How to Run



&nbsp;Run the complete example:

```bash

cd scripts

python ab\_testing\_simulation.py

