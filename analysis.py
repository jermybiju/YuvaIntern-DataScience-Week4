
"""
YuvaIntern Week 4 — Machine Learning Model Development
Steps 2 + 3: Data prep + 3 models (Logistic Regression, Decision Tree, Random Forest)
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                              f1_score, confusion_matrix, classification_report,
                              roc_curve, roc_auc_score)

# Load cleaned dataset
df = pd.read_csv("data/titanic_cleaned.csv")
os.makedirs("images", exist_ok=True)
sns.set_style("whitegrid")

print("=" * 60)
print("WEEK 4 — MACHINE LEARNING MODEL DEVELOPMENT")
print("=" * 60)

# ---------- Data Preparation ----------
print("\n--- Data Preparation ---")
print(f"Original shape: {df.shape}")

features = ['pclass', 'sex', 'age', 'sibsp', 'parch', 'fare', 'embarked']
target = 'survived'

df_ml = df[features + [target]].copy()
df_ml['sex'] = df_ml['sex'].map({'male': 0, 'female': 1})
df_ml = pd.get_dummies(df_ml, columns=['embarked'], prefix='embarked', drop_first=True)

print(f"After encoding shape: {df_ml.shape}")
print(f"Columns: {df_ml.columns.tolist()}")
print(f"Missing values: {df_ml.isnull().sum().sum()}")

X = df_ml.drop(columns=[target])
y = df_ml[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

print(f"\nTrain set: {X_train.shape[0]} samples")
print(f"Test set:  {X_test.shape[0]} samples")
print(f"Train survival rate: {y_train.mean():.3f}")
print(f"Test survival rate:  {y_test.mean():.3f}")

scaler = StandardScaler()
num_cols = ['age', 'fare', 'sibsp', 'parch']
X_train_scaled = X_train.copy()
X_test_scaled = X_test.copy()
X_train_scaled[num_cols] = scaler.fit_transform(X_train[num_cols])
X_test_scaled[num_cols] = scaler.transform(X_test[num_cols])

metrics = {}

# ==================================================================
# MODEL 1: LOGISTIC REGRESSION
# ==================================================================
print("\n" + "=" * 60)
print("MODEL 1 — LOGISTIC REGRESSION")
print("=" * 60)

log_reg = LogisticRegression(random_state=42, max_iter=1000)
log_reg.fit(X_train_scaled, y_train)

y_pred_lr = log_reg.predict(X_test_scaled)
y_proba_lr = log_reg.predict_proba(X_test_scaled)[:, 1]

acc = accuracy_score(y_test, y_pred_lr)
prec = precision_score(y_test, y_pred_lr)
rec = recall_score(y_test, y_pred_lr)
f1 = f1_score(y_test, y_pred_lr)
auc = roc_auc_score(y_test, y_proba_lr)

print(f"Accuracy:  {acc:.4f}")
print(f"Precision: {prec:.4f}")
print(f"Recall:    {rec:.4f}")
print(f"F1 Score:  {f1:.4f}")
print(f"ROC AUC:   {auc:.4f}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred_lr, target_names=['Did Not Survive', 'Survived']))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred_lr))

metrics['Logistic Regression'] = {
    'Accuracy': acc, 'Precision': prec, 'Recall': rec, 'F1': f1, 'AUC': auc
}


# ==================================================================
# MODEL 2: DECISION TREE
# ==================================================================
print("\n" + "=" * 60)
print("MODEL 2 — DECISION TREE")
print("=" * 60)

dt = DecisionTreeClassifier(random_state=42, max_depth=5, min_samples_leaf=5)
dt.fit(X_train_scaled, y_train)

y_pred_dt = dt.predict(X_test_scaled)
y_proba_dt = dt.predict_proba(X_test_scaled)[:, 1]

acc_dt = accuracy_score(y_test, y_pred_dt)
prec_dt = precision_score(y_test, y_pred_dt)
rec_dt = recall_score(y_test, y_pred_dt)
f1_dt = f1_score(y_test, y_pred_dt)
auc_dt = roc_auc_score(y_test, y_proba_dt)

print(f"Accuracy:  {acc_dt:.4f}")
print(f"Precision: {prec_dt:.4f}")
print(f"Recall:    {rec_dt:.4f}")
print(f"F1 Score:  {f1_dt:.4f}")
print(f"ROC AUC:   {auc_dt:.4f}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred_dt, target_names=['Did Not Survive', 'Survived']))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred_dt))

metrics['Decision Tree'] = {
    'Accuracy': acc_dt, 'Precision': prec_dt, 'Recall': rec_dt,
    'F1': f1_dt, 'AUC': auc_dt
}


# ==================================================================
# MODEL 3: RANDOM FOREST
# ==================================================================
print("\n" + "=" * 60)
print("MODEL 3 — RANDOM FOREST")
print("=" * 60)

rf = RandomForestClassifier(n_estimators=200, max_depth=6,
                             min_samples_leaf=3, random_state=42)
rf.fit(X_train_scaled, y_train)

y_pred_rf = rf.predict(X_test_scaled)
y_proba_rf = rf.predict_proba(X_test_scaled)[:, 1]

acc_rf = accuracy_score(y_test, y_pred_rf)
prec_rf = precision_score(y_test, y_pred_rf)
rec_rf = recall_score(y_test, y_pred_rf)
f1_rf = f1_score(y_test, y_pred_rf)
auc_rf = roc_auc_score(y_test, y_proba_rf)

print(f"Accuracy:  {acc_rf:.4f}")
print(f"Precision: {prec_rf:.4f}")
print(f"Recall:    {rec_rf:.4f}")
print(f"F1 Score:  {f1_rf:.4f}")
print(f"ROC AUC:   {auc_rf:.4f}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred_rf, target_names=['Did Not Survive', 'Survived']))

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred_rf))

metrics['Random Forest'] = {
    'Accuracy': acc_rf, 'Precision': prec_rf, 'Recall': rec_rf,
    'F1': f1_rf, 'AUC': auc_rf
}


# ==================================================================
# MODEL COMPARISON
# ==================================================================
print("\n" + "=" * 60)
print("MODEL COMPARISON")
print("=" * 60)

metrics_df = pd.DataFrame(metrics).T
print(metrics_df.round(4).to_string())

best_model_name = metrics_df['Accuracy'].idxmax()
print(f"\nBest model by accuracy: {best_model_name} ({metrics_df.loc[best_model_name, 'Accuracy']:.4f})")

# Save metrics
with open('metrics.json', 'w') as f:
    json.dump(metrics, f, indent=2)
print("\nMetrics saved to metrics.json")


# ==================================================================
# STEP 4: VISUALIZATIONS
# ==================================================================

# ---------- Chart 1: Confusion Matrices (all 3 models) ----------
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
models_list = [
    ('Logistic Regression', y_pred_lr),
    ('Decision Tree', y_pred_dt),
    ('Random Forest', y_pred_rf),
]
for ax, (name, y_pred) in zip(axes, models_list):
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
                cbar=False, xticklabels=['Did Not Survive', 'Survived'],
                yticklabels=['Did Not Survive', 'Survived'])
    ax.set_title(f'{name}\nAccuracy: {accuracy_score(y_test, y_pred):.3f}')
    ax.set_xlabel('Predicted')
    ax.set_ylabel('Actual')
plt.tight_layout()
plt.savefig('images/week4_chart1_confusion_matrices.png', dpi=150)
plt.close()
print("Chart 1 saved: images/week4_chart1_confusion_matrices.png")


# ---------- Chart 2: ROC Curves (all 3 models) ----------
fig, ax = plt.subplots(figsize=(8, 6))
for name, y_proba, color in [
    ('Logistic Regression', y_proba_lr, '#4C72B0'),
    ('Decision Tree', y_proba_dt, '#DD8452'),
    ('Random Forest', y_proba_rf, '#55A868'),
]:
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    auc_val = roc_auc_score(y_test, y_proba)
    ax.plot(fpr, tpr, color=color, linewidth=2,
            label=f'{name} (AUC = {auc_val:.3f})')
ax.plot([0, 1], [0, 1], 'k--', linewidth=1, label='Random (AUC = 0.500)')
ax.set_xlabel('False Positive Rate', fontsize=11)
ax.set_ylabel('True Positive Rate', fontsize=11)
ax.set_title('ROC Curves — Model Comparison', fontsize=13, fontweight='bold')
ax.legend(loc='lower right')
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('images/week4_chart2_roc_curves.png', dpi=150)
plt.close()
print("Chart 2 saved: images/week4_chart2_roc_curves.png")


# ---------- Chart 3: Metrics Comparison ----------
metrics_df = pd.DataFrame(metrics).T
fig, ax = plt.subplots(figsize=(10, 5))
metrics_df.plot(kind='bar', ax=ax, width=0.8,
                color=['#4C72B0', '#DD8452', '#55A868', '#C44E52', '#8172B2'])
ax.set_title('Model Performance Metrics Comparison', fontsize=13, fontweight='bold')
ax.set_ylabel('Score', fontsize=11)
ax.set_xlabel('Model', fontsize=11)
ax.set_ylim(0, 1)
ax.legend(title='Metric', loc='lower right', ncol=2)
plt.xticks(rotation=0)
for container in ax.containers:
    ax.bar_label(container, fmt='%.2f', padding=2, fontsize=8)
plt.tight_layout()
plt.savefig('images/week4_chart3_metrics_comparison.png', dpi=150)
plt.close()
print("Chart 3 saved: images/week4_chart3_metrics_comparison.png")


# ---------- Chart 4: Feature Importance (Random Forest) ----------
importances = pd.Series(rf.feature_importances_, index=X.columns).sort_values()
fig, ax = plt.subplots(figsize=(9, 5))
importances.plot(kind='barh', ax=ax, color='#55A868')
ax.set_title('Feature Importance (Random Forest)', fontsize=13, fontweight='bold')
ax.set_xlabel('Importance', fontsize=11)
ax.set_ylabel('Feature', fontsize=11)
for i, v in enumerate(importances):
    ax.text(v + 0.005, i, f'{v:.3f}', va='center', fontsize=9)
plt.tight_layout()
plt.savefig('images/week4_chart4_feature_importance.png', dpi=150)
plt.close()
print("Chart 4 saved: images/week4_chart4_feature_importance.png")


# ---------- Chart 5: Learning Curve (Random Forest) ----------
from sklearn.model_selection import learning_curve
train_sizes, train_scores, test_scores = learning_curve(
    RandomForestClassifier(n_estimators=200, max_depth=6, min_samples_leaf=3, random_state=42),
    X_train_scaled, y_train, cv=5, n_jobs=-1,
    train_sizes=np.linspace(0.1, 1.0, 10), scoring='accuracy'
)
train_mean = train_scores.mean(axis=1)
train_std = train_scores.std(axis=1)
test_mean = test_scores.mean(axis=1)
test_std = test_scores.std(axis=1)

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(train_sizes, train_mean, 'o-', color='#4C72B0', label='Training score')
ax.fill_between(train_sizes, train_mean - train_std, train_mean + train_std,
                alpha=0.15, color='#4C72B0')
ax.plot(train_sizes, test_mean, 'o-', color='#C44E52', label='Cross-validation score')
ax.fill_between(train_sizes, test_mean - test_std, test_mean + test_std,
                alpha=0.15, color='#C44E52')
ax.set_title('Learning Curve — Random Forest', fontsize=13, fontweight='bold')
ax.set_xlabel('Training Set Size', fontsize=11)
ax.set_ylabel('Accuracy Score', fontsize=11)
ax.legend(loc='lower right')
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('images/week4_chart5_learning_curve.png', dpi=150)
plt.close()
print("Chart 5 saved: images/week4_chart5_learning_curve.png")