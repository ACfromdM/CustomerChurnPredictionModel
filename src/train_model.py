# Train/test split, model fitting & tuning

import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from pathlib import Path

def load_data(path: Path):
    return pd.read_csv(path / 'churn_dataset.csv')


def train_and_save(df, model_path: Path):
    X = df.drop(columns=['customer_id','churned'])
    y = df['churned']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y)

    clf = RandomForestClassifier(random_state=42)
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [None, 10, 20]
    }
    grid = GridSearchCV(clf, param_grid, cv=5, scoring='roc_auc', n_jobs=-1)
    grid.fit(X_train, y_train)

    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({'model': grid.best_estimator_, 'X_test': X_test, 'y_test': y_test},
                model_path)
    print(f"Best params: {grid.best_params_}")

if __name__ == '__main__':
    df = load_data(Path('data/processed'))
    train_and_save(df, Path('models/churn_rf.joblib'))
