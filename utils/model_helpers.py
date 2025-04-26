import pickle
import pandas as pd
import plotly.graph_objs as go
from database.db_connection import Transaction  # Add this import
from database.db_connection import db, Transaction
from datetime import datetime, timedelta
def predict_clv():
    # 1. Fetch real transaction data
    transactions = db.session.query(Transaction.hshd_num, Transaction.spend).limit(50000).all()
    df = pd.DataFrame(transactions, columns=['hshd_num', 'spend'])

    # 2. Aggregate by customer
    agg = df.groupby('hshd_num').agg(
        total_spend=('spend', 'sum'),
        num_purchases=('spend', 'count'),
        avg_spend=('spend', 'mean')
    ).reset_index()

    # 3. Load your model
    model = pickle.load(open('models/clv_model.pkl', 'rb'))

    # 4. Predict CLV
    X_real = agg[['total_spend', 'num_purchases', 'avg_spend']]
    y_pred = model.predict(X_real)

    # 5. Plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=agg['hshd_num'], y=y_pred, mode='lines+markers', name='Predicted CLV'))

    # Update layout
    fig.update_layout(
        title='Real Customer Lifetime Value Prediction',
        xaxis_title='Household Number',
        yaxis_title='Predicted CLV',
        yaxis=dict(dtick=500)# You can customize the tick format if you need
    )

    return fig.to_html(full_html=False)




def predict_churn():
    # Fetch latest purchase date per household
    data = db.session.query(Transaction.hshd_num, Transaction.purchase_).limit(50000).all()


    df = pd.DataFrame(data, columns=['hshd_num', 'purchase_'])
    df['purchase_'] = pd.to_datetime(df['purchase_'])

    # Find the last purchase date for each household
    last_purchase = df.groupby('hshd_num')['purchase_'].max().reset_index()

    # Define churn threshold: 30 days ago from today
    latest_purchase_date = last_purchase['purchase_'].max()
    churn_threshold = latest_purchase_date - timedelta(days=30)

    # Classify
    last_purchase['churned'] = last_purchase['purchase_'] < churn_threshold

    churned_count = last_purchase['churned'].sum()
    active_count = len(last_purchase) - churned_count
    print(f"Total households analyzed: {len(last_purchase)}")
    print(f"Active Customers: {active_count}")
    print(f"Churned Customers: {churned_count}")
    print(df['purchase_'].describe())
    # Plot
    labels = ['Active Customers', 'Churned Customers']
    values = [active_count, churned_count]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(title='Customer Churn Analysis (Real Data)')

    return fig.to_html(full_html=False)


def analyze_basket():
    # ⚡ Optimized: only load needed fields
    transactions = db.session.query(Transaction.hshd_num, Transaction.product_num).limit(5000).all()
    df = pd.DataFrame(transactions, columns=['hshd_num', 'product_num'])


    top_products = df['product_num'].value_counts().head(5)

    fig = go.Figure([go.Bar(x=top_products.index.astype(str), y=top_products.values)])
    fig.update_layout(title='Top 5 Most Purchased Products', xaxis_title='Product Number', yaxis_title='Purchase Count')

    return fig.to_html(full_html=False)
