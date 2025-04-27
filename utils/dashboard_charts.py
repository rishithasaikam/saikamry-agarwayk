import pandas as pd
import plotly.graph_objs as go
from database.db_connection import Transaction, Product
from database.db_connection import db, Transaction, Product

def plot_spend_over_time():
    from database.db_connection import db, Transaction
    import pandas as pd
    import plotly.graph_objs as go

    latest_year = db.session.query(db.func.max(Transaction.year)).scalar()
    data = db.session.query(Transaction.purchase_, Transaction.spend)\
            .filter(Transaction.year == latest_year).all()

    df = pd.DataFrame(data, columns=['purchase_date', 'spend'])
    df['purchase_date'] = pd.to_datetime(df['purchase_date'])
    latest_year = df['purchase_date'].dt.year.max()
    df = df[df['purchase_date'].dt.year == latest_year]

    monthly_spend = df.groupby(df['purchase_date'].dt.month)['spend'].sum().reset_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=monthly_spend['purchase_date'], y=monthly_spend['spend'], mode='lines+markers'))
    fig.update_layout(title=f'Monthly Spend Trend ({latest_year})', xaxis_title='Month', yaxis_title='Total Spend')

    return fig.to_html(full_html=False)



def plot_brand_preference():
    from database.db_connection import db, Transaction, Product
    import pandas as pd
    import plotly.graph_objs as go

    latest_year = db.session.query(db.func.max(Transaction.year)).scalar()

    data = db.session.query(Product.brand_ty)\
           .join(Transaction, Transaction.product_num == Product.product_num)\
           .filter(Transaction.year == latest_year).limit(10000).all()

    df = pd.DataFrame(data, columns=['brand_ty'])
    brand_counts = df['brand_ty'].value_counts()

    fig = go.Figure([go.Bar(x=brand_counts.index, y=brand_counts.values)])
    fig.update_layout(title=f'Brand Preference ({latest_year})',
                      xaxis_title='Brand Type',
                      yaxis_title='Count')

    return fig.to_html(full_html=False)



def plot_top_categories_over_time():
    from database.db_connection import db, Transaction, Product

    # Join products and transactions
    data = db.session.query(
        Transaction.purchase_,
        Product.department,
        Transaction.spend
    ).join(Product, Transaction.product_num == Product.product_num)\
     .limit(10000).all()

    df = pd.DataFrame(data, columns=['purchase_date', 'department', 'spend'])
    df['purchase_date'] = pd.to_datetime(df['purchase_date'])
    df['year'] = df['purchase_date'].dt.year
    df['year_month'] = df['purchase_date'].dt.to_period('M')

    # Filter for most recent year
    if not df.empty:
        latest_year = df['year'].max()
        df = df[df['year'] == latest_year]

    # Top 5 departments by total spend (only from the latest year)
    top_departments = df.groupby('department')['spend'].sum().nlargest(5).index.tolist()
    df_top = df[df['department'].isin(top_departments)]

    pivot = df_top.pivot_table(index='year_month', columns='department', values='spend', aggfunc='sum').fillna(0)

    fig = go.Figure()
    for dept in pivot.columns:
        fig.add_trace(go.Scatter(x=pivot.index.astype(str), y=pivot[dept], mode='lines+markers', name=dept))

    fig.update_layout(
        title=f'Spend by Top 5 Categories Over Time ({latest_year})',
        xaxis_title='Month',
        yaxis_title='Total Spend'
    )

    return fig.to_html(full_html=False)

