
import numpy as np
import pandas as pd
import os


from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import PowerTransformer, MinMaxScaler, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import recall_score, f1_score, classification_report



def create_data(file):
    data = pd.read_csv(file)
    return data


def clean_data(data):
    cp_dummies = pd.get_dummies(data['cp'], drop_first=True, prefix='cp')
    thal_dummies = pd.get_dummies(data['thal'], drop_first=True, prefix='thal')
    ecg_dummies = pd.get_dummies(data['restecg'], drop_first=False, prefix='ecg')
    slope_dummies = pd.get_dummies(data['slope'], drop_first=True, prefix='slope')
    ca_dummies = pd.get_dummies(data['ca'], drop_first=False, prefix='ca')
    data = pd.merge(left=data, right=cp_dummies, how='left', left_index=True, right_index=True)
    data = pd.merge(left=data, right=thal_dummies, how='left', left_index=True, right_index=True)
    data = pd.merge(left=data, right=ecg_dummies, how='left', left_index=True, right_index=True)
    data = pd.merge(left=data, right=slope_dummies, how='left', left_index=True, right_index=True)
    data = pd.merge(left=data, right=ca_dummies, how='left', left_index=True, right_index=True)

    data['log_chol'] = np.log(data['chol'])
    data['log_age'] = np.log(data['age'])
    data['log_thalach'] = np.log(data['thalach'])
    data['log_trestbps'] = np.log(data['trestbps'])
    data['old_peak'] = (data['oldpeak'] - data['oldpeak'].min()) / (data['oldpeak'].max() - data['oldpeak'].min())

    drop_cols = ['thalach', 'oldpeak', 'thal', 'trestbps', 'chol', 'cp', 'restecg', "slope", "age"]
    data = data.drop(drop_cols, axis=1)
    return data



def grid_search_rf(df):
    X, y = df.drop('target', axis=1), df['target']

    param_grid = {
        'n_estimators': [100, 300],

        'max_features': ['auto'],

        'max_depth': [4, 5],

        'criterion': ['gini']
    }

    cv = GridSearchCV(estimator=RandomForestClassifier(random_state=66),
                      param_grid=param_grid,
                      scoring='recall',
                      cv=5)
    cv.fit(X, y)

    return cv.best_params_


def rf_model(data, plot_importance=False):
    X, y = data.drop('target', axis=1), data['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=66)

    model = RandomForestClassifier(n_estimators=300,
                                   max_depth=4,
                                   max_features='auto',
                                   criterion='gini',
                                   random_state=66)

    model.fit(X_train, y_train)

    train_preds = model.predict(X_train)
    test_preds = model.predict(X_test)

    train_recall = recall_score(y_train, train_preds)
    test_recall = recall_score(y_test, test_preds)

    cr = classification_report(y_test, test_preds)
    probs = model.predict_proba(X_test)

    # create a df of feature importance
    columns = X.columns
    imp = model.feature_importances_
    imp_df = pd.DataFrame({"feature": columns, "importance": imp})
    imp_df = imp_df.sort_values(by="importance", ascending=True)

    results = {"train_recall": train_recall,
               "test_recall": test_recall,
               "classification_report": cr,
               "Probabilites": probs[0],
               "model_importance": imp_df}



    return results




print(f"----->Load and clean data")
df = create_data("sample_data_heart.csv")
print(df.head())
df = clean_data(df)
print(df.head())
print(f"----->Load and clean data complete")

print(f"----->Grid search")
grid_search_rf(df)
print(f"----->Grid search complete")

print(f"----->Final model")
r = rf_model(df, plot_importance=False)
print(r)
print(f"----->Final model complete")

print(f"----->Results")
print(f"Train recall score: {round(r['train_recall'], 2)}")
print(f"Test recall score: {round(r['test_recall'])}")
print("\n")
print(r["classification_report"])
print(f"----->Results complete")



