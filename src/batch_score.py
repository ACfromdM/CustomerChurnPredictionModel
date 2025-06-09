import pandas as pd
import joblib
from pathlib import Path


def load_new_data(path: Path):
    return pd.read_csv(path / 'new_customers.csv')


def score_and_save(new_df, model_artifact_path: str, output_path: Path):
    artifact = joblib.load(model_artifact_path)
    model = artifact['model']

    X_new = new_df.drop(columns=['customer_id'])
    new_df['churn_proba'] = model.predict_proba(X_new)[:,1]

    output_path.mkdir(parents=True, exist_ok=True)
    new_df.to_csv(output_path / 'churn_scores.csv', index=False)

if __name__ == '__main__':
    new_data = load_new_data(Path('data/raw'))
    score_and_save(new_data, 'models/churn_rf.joblib', Path('data/scores'))