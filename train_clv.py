# train_clv_model.py

import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor
from database.db_connection import db, Transaction
from app import app  # Import your Flask app

with app.app_context():
    # Step 1: Fetch data (recent year transactions)
    latest_year = db.session.query(db.func.max(Transaction.year)).scalar()

    data = db.session.query(Transaction.hshd_num, Transaction.spend)\
            .filter(Transaction.year == latest_year).all()

    df = pd.DataFrame(data, columns=['hshd_num', 'spend'])

    # Step 2: Aggregate customer metrics
    agg = df.groupby('hshd_num').agg(
        total_spend=('spend', 'sum'),
        num_purchases=('spend', 'count'),
        avg_spend=('spend', 'mean')
    ).reset_index()

    # Step 3: Create feature matrix (X) and target (y)
    X = agg[['total_spend', 'num_purchases', 'avg_spend']]

    # Dummy CLV target: total_spend * 1.2
    agg['clv'] = agg['total_spend'] * 1.2
    y = agg['clv']

    # Step 4: Train the model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Step 5: Save the model
    with open('models/clv_model.pkl', 'wb') as f:
        pickle.dump(model, f)

    print("✅ CLV model trained and saved successfully!")
