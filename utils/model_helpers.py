import pickle
import pandas as pd
import plotly.graph_objs as go
from database.db_connection import Transaction  # Add this import
from database.db_connection import db, Transaction
from datetime import datetime, timedelta
def predict_clv():
    from database.db_connection import db, Transaction
    import pandas as pd
    import pickle
    import plotly.graph_objs as go
    from datetime import datetime

    # Fetch recent year only
    latest_year = db.session.query(db.func.max(Transaction.year)).scalar()
    transactions = db.session.query(Transaction.hshd_num, Transaction.spend)\
                    .filter(Transaction.year == latest_year).all()

    df = pd.DataFrame(transactions, columns=['hshd_num', 'spend'])

    # Aggregate by customer
    agg = df.groupby('hshd_num').agg(
        total_spend=('spend', 'sum'),
        num_purchases=('spend', 'count'),
        avg_spend=('spend', 'mean')
    ).reset_index()

    model = pickle.load(open('models/clv_model.pkl', 'rb'))

    X_real = agg[['total_spend', 'num_purchases', 'avg_spend']]
    y_pred = model.predict(X_real)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=agg['hshd_num'], y=y_pred, mode='lines+markers', name='Predicted CLV'))
    fig.update_layout(title=f'Real Customer Lifetime Value Prediction ({latest_year})',
                      xaxis_title='Household Number',
                      yaxis_title='Predicted CLV')

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
    # Plot
    labels = ['Active Customers', 'Churned Customers']
    values = [active_count, churned_count]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(title='Customer Churn Analysis (Real Data)')

    return fig.to_html(full_html=False)


def analyze_basket():
    from database.db_connection import db, Transaction
    import pandas as pd
    import plotly.graph_objs as go

    latest_year = db.session.query(db.func.max(Transaction.year)).scalar()
    transactions = db.session.query(Transaction.hshd_num, Transaction.product_num)\
                    .filter(Transaction.year == latest_year).limit(10000).all()

    df = pd.DataFrame(transactions, columns=['hshd_num', 'product_num'])

    top_products = df['product_num'].value_counts().head(10)

    fig = go.Figure([go.Bar(x=top_products.index.astype(str), y=top_products.values)])
    fig.update_layout(title=f'Top 10 Purchased Products ({latest_year})',
                      xaxis_title='Product Number',
                      yaxis_title='Count')

    return fig.to_html(full_html=False)

