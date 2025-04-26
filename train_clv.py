# train_clv_model.py

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle
from database.db_connection import db, Transaction
from config import DATABASE_URI

from flask import Flask
from database.db_connection import db

# Flask App Setup (to use database)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    # Fetch data
    transactions = db.session.query(Transaction.hshd_num, Transaction.spend, Transaction.basket_num).limit(50000).all()

    df = pd.DataFrame(transactions, columns=['hshd_num', 'spend', 'basket_num'])

    # Aggregate features
    agg = df.groupby('hshd_num').agg(
        total_spend=('spend', 'sum'),
        num_purchases=('basket_num', 'count'),
        avg_spend=('spend', 'mean')
    ).reset_index()

    # Features (X) and Target (y)
    X_train = agg[['total_spend', 'num_purchases', 'avg_spend']]
    y_train = agg['total_spend'] * 1.2  # (Fake target now, can replace later if needed)

    # Train Model
    model = RandomForestRegressor()
    model.fit(X_train, y_train)

    # Save model
    with open('models/clv_model.pkl', 'wb') as f:
        pickle.dump(model, f)

    print("✅ Model trained and saved successfully!")
