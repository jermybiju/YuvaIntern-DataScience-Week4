"""
YuvaIntern Week 4 Report Generator
Machine Learning Model Development and Evaluation
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


def add_code_block(doc, code_text):
    para = doc.add_paragraph()
    para.paragraph_format.left_indent = Inches(0.25)
    para.paragraph_format.space_before = Pt(1)
    para.paragraph_format.space_after = Pt(2)
    run = para.add_run(code_text)
    run.font.name = 'Courier New'
    run.font.size = Pt(7)
    pPr = para._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), 'F2F2F2')
    pPr.append(shd)


def add_table(doc, headers, rows):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = 'Light Grid Accent 1'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for row in table.rows:
        tr = row._tr
        trPr = tr.get_or_add_trPr()
        cantSplit = OxmlElement('w:cantSplit')
        trPr.append(cantSplit)
    hdr = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = str(h)
        for p in hdr[i].paragraphs:
            for r in p.runs:
                r.font.bold = True
                r.font.size = Pt(10)
    for row_data in rows:
        cells = table.add_row().cells
        for i, val in enumerate(row_data):
            cells[i].text = str(val)
            for p in cells[i].paragraphs:
                for r in p.runs:
                    r.font.size = Pt(10)
    for row in table.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                paragraph.paragraph_format.keep_with_next = True
    doc.add_paragraph()


def add_bullet(doc, text):
    doc.add_paragraph(text, style='List Bullet')


def add_image_with_caption(doc, img_path, caption, width=5.5):
    if os.path.exists(img_path):
        doc.add_picture(img_path, width=Inches(width))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap = doc.add_paragraph()
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = cap.add_run(caption)
        run.font.italic = True
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)


# ------------------------------------------------------------------
# Build document
# ------------------------------------------------------------------

doc = Document()
style = doc.styles['Normal']
style.font.name = 'Calibri'
style.font.size = Pt(11)

# ---------- Title page ----------
doc.add_paragraph('\n\n')
t = doc.add_paragraph()
t.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = t.add_run('YuvaIntern')
r.font.size = Pt(20); r.font.bold = True; r.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)

s = doc.add_paragraph()
s.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = s.add_run('Virtual Data Science with Python Apprentice Internship')
r.font.size = Pt(14); r.font.italic = True

doc.add_paragraph()

h = doc.add_paragraph()
h.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = h.add_run('WEEK 4 REPORT')
r.font.size = Pt(16); r.font.bold = True

h = doc.add_paragraph()
h.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = h.add_run('Machine Learning Model Development and Evaluation')
r.font.size = Pt(15); r.font.bold = True; r.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)

h = doc.add_paragraph()
h.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = h.add_run('Predicting Titanic Survival with Three Classification Models')
r.font.size = Pt(12); r.font.italic = True

doc.add_paragraph('\n\n')

info = doc.add_table(rows=0, cols=2)
info.alignment = WD_TABLE_ALIGNMENT.CENTER
rows = [
    ('Submitted by', 'Jermy Biju'),
    ('Role', 'Virtual Data Science with Python Apprentice Intern'),
    ('Organization', 'YuvaIntern'),
    ('Internship Duration', 'August 24, 2026 – September 28, 2026'),
    ('Week 4 Duration', '30 – 35 hours'),
    ('Dataset', 'Titanic (cleaned in Week 1, 889 rows x 14 columns)'),
    ('Tools', 'Python 3.14, Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn'),
]
for k, v in rows:
    cells = info.add_row().cells
    cells[0].text = k; cells[1].text = v
    for p in cells[0].paragraphs:
        for r in p.runs:
            r.font.bold = True; r.font.size = Pt(11)
    for p in cells[1].paragraphs:
        for r in p.runs:
            r.font.size = Pt(11)

doc.add_page_break()


# ---------- 1. Executive Summary ----------
doc.add_heading('1. Executive Summary', level=1)
doc.add_paragraph(
    'This report presents Week 4 of the YuvaIntern Virtual Data Science with Python '
    'Apprenticeship. The task was to build and evaluate a basic machine learning model '
    'on a publicly available dataset. Three classification models were trained and '
    'evaluated to predict passenger survival on the Titanic: Logistic Regression, '
    'Decision Tree, and Random Forest.'
)
doc.add_paragraph('Summary of results:')
add_bullet(doc, 'Logistic Regression: 82.6% accuracy, ROC AUC 0.860 (best overall).')
add_bullet(doc, 'Random Forest: 81.5% accuracy, ROC AUC 0.850 (best precision at 0.83).')
add_bullet(doc, 'Decision Tree: 77.0% accuracy, ROC AUC 0.837 (weakest).')
doc.add_paragraph(
    'The simplest model, Logistic Regression, performed best by accuracy and AUC, '
    'suggesting that the underlying relationships in this dataset are largely linear. '
    'Feature importance analysis from the Random Forest identified sex, fare, age, and '
    'passenger class as the four most predictive features, confirming the statistical '
    'associations found in Week 3. A learning curve analysis showed no severe overfitting, '
    'with training and cross-validation scores staying within reasonable bounds.'
)


# ---------- 2. Introduction ----------
doc.add_heading('2. Introduction — Why Machine Learning?', level=1)
doc.add_paragraph(
    'Weeks 1 through 3 built up to this point. In Week 1 the dataset was cleaned and '
    'prepared. In Week 2 the survival patterns were visualized. In Week 3 those patterns '
    'were tested statistically. Week 4 completes the cycle by asking a predictive question: '
    'given what we know about a passenger, can we predict whether they survived?'
)
doc.add_paragraph(
    'Machine learning models learn patterns from historical data and apply those patterns '
    'to new, unseen observations. This report builds three such models and evaluates them '
    'using standard classification metrics. The goal is not simply to achieve the highest '
    'accuracy, but to understand the trade-offs between different models and to be honest '
    'about each model\'s limitations.'
)
doc.add_page_break() 


# ---------- 3. Dataset ----------
doc.add_heading('3. Dataset and Preprocessing', level=1)
doc.add_paragraph(
    'The dataset is the cleaned Titanic dataset from Week 1: 889 passengers, 14 columns, '
    'with zero missing values. The target variable is survived (0 or 1).'
)

doc.add_heading('3.1 Feature selection', level=2)
doc.add_paragraph('Seven features were selected for the model:')
add_table(doc,
          ['Feature', 'Type', 'Handling'],
          [
              ('pclass', 'Ordinal (1/2/3)', 'Used directly'),
              ('sex', 'Categorical', 'Mapped to 0 (male) / 1 (female)'),
              ('age', 'Continuous', 'Standardized (mean=0, std=1)'),
              ('sibsp', 'Integer', 'Standardized'),
              ('parch', 'Integer', 'Standardized'),
              ('fare', 'Continuous', 'Standardized'),
              ('embarked', 'Categorical', 'One-hot encoded (drop_first=True)'),
          ])

doc.add_paragraph('Redundant columns dropped: alive (identical to survived), class (same as pclass), who, adult_male, embark_town, alone.')

doc.add_heading('3.2 Train/test split', level=2)
add_table(doc,
          ['Split', 'Samples', 'Survival Rate'],
          [
              ('Training set', '711', '0.383'),
              ('Test set', '178', '0.382'),
          ])
doc.add_paragraph(
    'An 80/20 stratified split was used (random_state=42). Stratification ensured that '
    'the survival rate was nearly identical in both subsets (0.383 vs 0.382), preventing '
    'sampling bias.'
)

doc.add_page_break()


# ---------- 4. Methodology ----------
doc.add_heading('4. Methodology — Model Selection', level=1)
doc.add_paragraph(
    'Three classification algorithms were chosen to compare different model families:'
)
add_table(doc,
          ['Model', 'Family', 'Why chosen'],
          [
              ('Logistic Regression', 'Linear',
               'Simple, interpretable baseline. Well suited when relationships are approximately linear.'),
              ('Decision Tree', 'Tree-based',
               'Interpretable, non-linear. Shows decision rules explicitly.'),
              ('Random Forest', 'Ensemble',
               'Combines many trees to reduce overfitting. Often strong on tabular data.'),
          ])

doc.add_paragraph('Hyperparameters (chosen to prevent overfitting on a small dataset):')
add_bullet(doc, 'Logistic Regression: max_iter=1000.')
add_bullet(doc, 'Decision Tree: max_depth=5, min_samples_leaf=5.')
add_bullet(doc, 'Random Forest: n_estimators=200, max_depth=6, min_samples_leaf=3.')

doc.add_paragraph('Evaluation metrics:')
add_bullet(doc, 'Accuracy — overall proportion of correct predictions.')
add_bullet(doc, 'Precision — proportion of positive predictions that were correct.')
add_bullet(doc, 'Recall — proportion of actual positives correctly identified.')
add_bullet(doc, 'F1 Score — harmonic mean of precision and recall.')
add_bullet(doc, 'ROC AUC — area under the ROC curve; measures ranking quality across thresholds.')

doc.add_page_break()


# ---------- 5. Results ----------
doc.add_heading('5. Results', level=1)


# --- 5.1 Confusion matrices ---
doc.add_heading('5.1 Confusion Matrices — Three Models Side by Side', level=2)
add_image_with_caption(doc,
    'images/week4_chart1_confusion_matrices.png',
    'Figure 1: Confusion matrices for the three models on the test set (n = 178).')

doc.add_paragraph(
    'Logistic Regression has the most balanced confusion matrix: it correctly identifies '
    '99 non-survivors and 48 survivors, with 11 false positives and 20 false negatives. '
    'Random Forest is the most conservative — it makes the fewest false positives (9) but '
    'misses more survivors (24 false negatives). Decision Tree is weakest overall, with '
    '19 false positives and 22 false negatives.'
)


# --- 5.2 ROC curves ---
doc.add_heading('5.2 ROC Curves', level=2)
add_image_with_caption(doc,
    'images/week4_chart2_roc_curves.png',
    'Figure 2: ROC curves for the three models. The dashed diagonal represents a random classifier.')
doc.add_page_break()
doc.add_paragraph('ROC AUC values:')
add_table(doc,
          ['Model', 'ROC AUC'],
          [
              ('Logistic Regression', '0.860'),
              ('Random Forest', '0.850'),
              ('Decision Tree', '0.837'),
              ('Random baseline', '0.500'),
          ])
doc.add_paragraph(
    'All three models are far above the random baseline. Logistic Regression has the '
    'highest AUC, meaning that across all possible classification thresholds it ranks '
    'survivors above non-survivors more reliably than the other models.'
)


# --- 5.3 Metrics comparison ---
doc.add_heading('5.3 Metrics Comparison', level=2)
add_image_with_caption(doc,
    'images/week4_chart3_metrics_comparison.png',
    'Figure 3: Accuracy, precision, recall, F1, and AUC for each model.')

doc.add_paragraph('Full metrics table:')
add_table(doc,
          ['Model', 'Accuracy', 'Precision', 'Recall', 'F1', 'AUC'],
          [
              ('Logistic Regression', '0.826', '0.814', '0.706', '0.756', '0.860'),
              ('Decision Tree', '0.770', '0.708', '0.677', '0.692', '0.837'),
              ('Random Forest', '0.815', '0.830', '0.647', '0.727', '0.850'),
          ])
doc.add_paragraph(
    'Observations: Logistic Regression leads on accuracy, F1, and AUC. Random Forest has '
    'the highest precision (0.83), meaning when it predicts survival it is more often '
    'right, but its recall is lower (0.65), meaning it misses more real survivors. This is '
    'the classic precision-recall trade-off, and the right choice depends on the business '
    'cost of each type of error.'
)


# --- 5.4 Feature importance ---
doc.add_heading('5.4 Feature Importance (Random Forest)', level=2)
add_image_with_caption(doc,
    'images/week4_chart4_feature_importance.png',
    'Figure 4: Relative importance of each feature in the Random Forest model.')

add_table(doc,
          ['Feature', 'Importance'],
          [
              ('sex', '0.417'),
              ('fare', '0.200'),
              ('age', '0.139'),
              ('pclass', '0.119'),
              ('sibsp', '0.049'),
              ('parch', '0.032'),
              ('embarked_S', '0.027'),
              ('embarked_Q', '0.016'),
          ])
doc.add_paragraph(
    'Four features account for roughly 87% of the model\'s decision power: sex, fare, age, '
    'and pclass. This is a strong cross-check on the statistical analysis from Week 3, '
    'which independently identified sex and pclass as the strongest predictors of survival. '
    'The remaining features (sibsp, parch, embarked) contribute very little.'
)


# --- 5.5 Learning curve ---
doc.add_heading('5.5 Learning Curve — Overfitting Check', level=2)
add_image_with_caption(doc,
    'images/week4_chart5_learning_curve.png',
    'Figure 5: Learning curve for the Random Forest model. Training and cross-validation scores track each other closely.')

doc.add_paragraph(
    'The learning curve shows that training accuracy (around 0.88) and cross-validation '
    'accuracy (around 0.81) stay within about 0.07 of each other across all training set '
    'sizes. This small gap indicates that the model is not severely overfitting. The '
    'cross-validation score plateaus around 400 training samples, suggesting that '
    'additional data would not meaningfully improve performance — the model has extracted '
    'most of the signal available in these features.'
)

doc.add_page_break()


# ---------- 6. Critical Discussion ----------
doc.add_heading('6. Critical Discussion', level=1)

doc.add_heading('6.1 Why Logistic Regression won', level=2)
doc.add_paragraph(
    'The simplest model won on this dataset. This is not unusual. The Titanic features '
    'are mostly linearly separable — sex, class, and fare together create a clear decision '
    'boundary. Tree-based models can overfit on small samples (889 rows), and even with '
    'hyperparameter limits, they struggled to beat the baseline. This is a useful lesson: '
    'more complex models are not always better.'
)

doc.add_heading('6.2 Sources of error', level=2)
add_bullet(doc, 'Small dataset. With only 178 test samples, a difference of 2-3 correct predictions can change accuracy by over 1%.')
add_bullet(doc, 'Missing cabin information. The deck column was dropped in Week 1 due to 77% missing values. Cabin location was likely very predictive of survival.')
add_bullet(doc, 'Imputed ages. Age was imputed by subgroup median in Week 1. This is a reasonable but imperfect substitute for real age.')
add_bullet(doc, 'Unmeasured variables. Variables like "whether the passenger had a lifeboat seat" are not in the data but would be strongly predictive.')
add_bullet(doc, 'Precision-recall trade-off. Even the best model misses 30% of actual survivors — a substantial error rate.')

doc.add_heading('6.3 Suggestions for improvement', level=2)
add_bullet(doc, 'Engineer more features. Titles extracted from names (Mr, Mrs, Miss, Master) strongly correlate with class and survival. Family size buckets (small/large) may also help.')
add_bullet(doc, 'Try gradient boosting. XGBoost and LightGBM often outperform Random Forest on tabular data.')
add_bullet(doc, 'Cross-validation tuning. Use grid search with 5-fold CV to tune hyperparameters more rigorously.')
add_bullet(doc, 'Handle class imbalance. 62% of passengers did not survive. Class weights or SMOTE could improve recall for the survivor class.')
add_bullet(doc, 'Collect more data. The learning curve suggests 400+ samples is the plateau, but more passengers (if available) could still help rare subgroups.')

doc.add_heading('6.4 What this analysis does not claim', level=2)
doc.add_paragraph(
    'The model predicts survival based on associations in this dataset. It does not '
    'explain why survival differed. The relationships are observational. A model that '
    'predicts survival does not demonstrate causation, and the predictions should not be '
    'interpreted as causal statements about what would have saved individual passengers.'
)


# ---------- 7. Conclusion ----------
doc.add_heading('7. Conclusion', level=1)
doc.add_paragraph(
    'Week 4 completed the data science cycle that began in Week 1. The cleaned dataset '
    'was used to train three classification models — Logistic Regression, Decision Tree, '
    'and Random Forest — to predict passenger survival. Logistic Regression achieved the '
    'highest accuracy (82.6%) and ROC AUC (0.860), followed closely by Random Forest '
    '(81.5% / 0.850). Decision Tree was the weakest at 77.0%.'
)
doc.add_paragraph(
    'Feature importance analysis independently confirmed the findings of Week 3: sex, '
    'fare, age, and pclass account for roughly 87% of the model\'s predictive power. The '
    'learning curve showed no severe overfitting, and the study concluded with a candid '
    'discussion of error sources and improvement paths. The exercise demonstrates that '
    'model development is as much about honest evaluation and clear documentation as it '
    'is about achieving a high score.'
)


# ---------- 8. Appendix ----------
doc.add_heading('8. Appendix — Key Code Snippets', level=1)

doc.add_heading('8.1 Data preparation', level=2)
add_code_block(doc, '''df_ml = df[features + [target]].copy()
df_ml['sex'] = df_ml['sex'].map({'male': 0, 'female': 1})
df_ml = pd.get_dummies(df_ml, columns=['embarked'],
                        prefix='embarked', drop_first=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)''')

doc.add_heading('8.2 Logistic Regression', level=2)
add_code_block(doc, '''from sklearn.linear_model import LogisticRegression
log_reg = LogisticRegression(random_state=42, max_iter=1000)
log_reg.fit(X_train_scaled, y_train)
y_pred = log_reg.predict(X_test_scaled)
y_proba = log_reg.predict_proba(X_test_scaled)[:, 1]''')

doc.add_heading('8.3 Decision Tree and Random Forest', level=2)
add_code_block(doc, '''from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

dt = DecisionTreeClassifier(max_depth=5, min_samples_leaf=5, random_state=42)
rf = RandomForestClassifier(n_estimators=200, max_depth=6,
                             min_samples_leaf=3, random_state=42)''')

doc.add_heading('8.4 Evaluation metrics', level=2)
add_code_block(doc, '''from sklearn.metrics import (accuracy_score, precision_score,
                             recall_score, f1_score, roc_auc_score)

acc = accuracy_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_proba)''')

doc.add_heading('8.5 Learning curve', level=2)
add_code_block(doc, '''from sklearn.model_selection import learning_curve
train_sizes, train_scores, test_scores = learning_curve(
    RandomForestClassifier(n_estimators=200, max_depth=6),
    X_train_scaled, y_train, cv=5,
    train_sizes=np.linspace(0.1, 1.0, 10), scoring='accuracy'
)''')


# ---------- Save ----------
os.makedirs('report', exist_ok=True)
out = 'report/YuvaIntern_Week4_Report.docx'
doc.save(out)
print(f"Report saved to: {out}")