# Extract, sort & plot importances

import joblib
import pandas as pd
import matplotlib.pyplot as plt


def plot_importances(model_artifact_path: str):
    artifact = joblib.load(model_artifact_path)
    model = artifact['model']
    X_test = artifact['X_test']

    feat_imp = pd.Series(model.feature_importances_, index=X_test.columns)
    feat_imp = feat_imp.sort_values(ascending=False)

    plt.figure()
    feat_imp.plot(kind='bar')
    plt.ylabel('Importance')
    plt.title('Feature Importances')
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    plot_importances('models/churn_rf.joblib')