# YuvaIntern — Data Science with Python (Week 4)

**Intern:** Jermy Biju
**Role:** Virtual Data Science with Python Apprentice Intern
**Organization:** YuvaIntern
**Internship Duration:** August 24, 2026 – September 28, 2026

## Week 4 Task
Machine Learning Model Development and Evaluation

## Dataset
Cleaned Titanic dataset from Week 1 (889 rows × 14 columns, zero missing values).

## What was done
Three classification models were trained and evaluated to predict passenger survival:

| Model | Accuracy | Precision | Recall | F1 | ROC AUC |
|-------|----------|-----------|--------|----|---------|
| **Logistic Regression** | **0.826** | 0.814 | 0.706 | 0.756 | **0.860** |
| Decision Tree | 0.770 | 0.708 | 0.677 | 0.692 | 0.837 |
| Random Forest | 0.815 | 0.830 | 0.647 | 0.727 | 0.850 |

Best model: **Logistic Regression** (82.6% accuracy, AUC 0.860).

## Visualizations (5)
1. Confusion matrices (all 3 models side by side)
2. ROC curves with AUC
3. Metrics comparison bar chart
4. Feature importance (Random Forest)
5. Learning curve (overfitting check)

## Project structure
YuvaIntern-DataScience-Week4/
├── data/
│ └── titanic_cleaned.csv
├── images/
│ ├── week4_chart1_confusion_matrices.png
│ ├── week4_chart2_roc_curves.png
│ ├── week4_chart3_metrics_comparison.png
│ ├── week4_chart4_feature_importance.png
│ └── week4_chart5_learning_curve.png
├── report/
│ └── YuvaIntern_Week4_Report.docx
├── analysis.py
├── week4_report.py
├── .gitignore
└── README.md

text

## Tools
Python 3.14, Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn, python-docx

## How to run
python analysis.py # trains 3 models and generates 5 charts
python week4_report.py # builds the DOCX report

text

## Key findings
- Logistic Regression outperformed tree-based models — relationships are largely linear.
- Feature importance confirmed Week 3 findings: sex, fare, age, pclass account for ~87% of predictive power.
- Learning curve shows no severe overfitting (train ≈ 0.88, CV ≈ 0.81).
- Precision-recall trade-off: Random Forest has best precision, LR best recall.

## Note
All findings are reported as statistical associations, not causal claims.

## Related repositories
- [Week 1 — Data Acquisition, Cleaning and EDA](https://github.com/jermybiju/YuvaIntern-DataScience-Week1)
- [Week 2 — Advanced Data Visualization and Storytelling](https://github.com/jermybiju/YuvaIntern-DataScience-Week2)
- [Week 3 — Statistical Analysis and Hypothesis Testing](https://github.com/jermybiju/YuvaIntern-DataScience-Week3)