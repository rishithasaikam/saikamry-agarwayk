import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

df = pd.read_csv("data/400_transactions.csv")
df['date'] = pd.to_datetime(df['date'])
latest_date = df['date'].max()

df_agg = df.groupby('hshd_num').agg({
    'spend': 'sum',
    'date': 'max'
}).reset_index()

df_agg['days_since_last_purchase'] = (latest_date - df_agg['date']).dt.days
df_agg['churned'] = df_agg['days_since_last_purchase'] > 90

X = df_agg[['spend', 'days_since_last_purchase']]
y = df_agg['churned']

X_train, X_test, y_train, y_test = train_test_split(X, y)
model = RandomForestClassifier().fit(X_train, y_train)
print("Churn model trained.")
