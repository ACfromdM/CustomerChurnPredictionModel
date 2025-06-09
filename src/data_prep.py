import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from pathlib import Path


def load_raw_data(raw_dir: Path):
    cust = pd.read_csv(raw_dir / 'customers.csv', parse_dates=['signup_date'])
    tx   = pd.read_csv(raw_dir / 'transactions_summary.csv', parse_dates=['last_transaction_date'])
    lbl  = pd.read_csv(raw_dir / 'churn_labels.csv')
    return cust, tx, lbl


def engineer_features(cust, tx):
    df = cust.merge(tx, on='customer_id')
    # days since signup
    df['customer_age_days'] = (pd.Timestamp.today() - df['signup_date']).dt.days
    return df


def preprocess(df, output_path: Path):
    # numeric imputation
    num_cols = ['age','num_transactions','total_spend','days_since_last','customer_age_days']
    imputer = SimpleImputer(strategy='median')
    df[num_cols] = imputer.fit_transform(df[num_cols])
    
    # encode categorical
    cat_cols = ['gender','region']
    encoder = OneHotEncoder(drop='first', sparse=False)
    cat_df = pd.DataFrame(
        encoder.fit_transform(df[cat_cols]),
        columns=encoder.get_feature_names_out(cat_cols),
        index=df.index
    )
    df = pd.concat([df.drop(columns=cat_cols), cat_df], axis=1)

    # scale numeric
    scaler = StandardScaler()
    df[num_cols] = scaler.fit_transform(df[num_cols])

    # save processed
    output_path.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path / 'churn_dataset.csv', index=False)


if __name__ == '__main__':
    raw_dir = Path('data/raw')
    out_dir = Path('data/processed')
    cust, tx, lbl = load_raw_data(raw_dir)
    df = engineer_features(cust, tx).merge(lbl, on='customer_id')
    preprocess(df, out_dir)