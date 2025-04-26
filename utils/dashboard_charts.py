import pandas as pd
import plotly.graph_objs as go
from database.db_connection import Transaction, Product
from database.db_connection import db, Transaction, Product

def plot_spend_over_time():
    from database.db_connection import db, Transaction
    import pandas as pd
    import plotly.graph_objs as go

    # Fetch purchase date and spend
    data = db.session.query(Transaction.purchase_, Transaction.spend).limit(5000).all()

    df = pd.DataFrame(data, columns=['purchase_date', 'spend'])

    # Convert purchase date to datetime
    df['purchase_date'] = pd.to_datetime(df['purchase_date'])

    # Extract YEAR and MONTH separately
    df['year_month'] = df['purchase_date'].dt.to_period('M')

    # Group by Year-Month and ONLY sum spend
    monthly_spend = df.groupby('year_month')['spend'].sum().reset_index()

    # Convert back to timestamp for plotting
    monthly_spend['year_month'] = monthly_spend['year_month'].dt.to_timestamp()

    # Plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=monthly_spend['year_month'], y=monthly_spend['spend'], mode='lines+markers'))
    fig.update_layout(
        title='Monthly Spend Over Time',
        xaxis_title='Month',
        yaxis_title='Total Spend',
        xaxis_tickformat='%b %Y'  # Display 'Sep 2018', etc.
    )

    return fig.to_html(full_html=False)


def plot_brand_preference():

    data = db.session.query(Product.brand_ty).limit(10000).all()
    df = pd.DataFrame(data, columns=['brand_ty'])

    brand_counts = df['brand_ty'].value_counts()

    fig = go.Figure([go.Bar(x=brand_counts.index, y=brand_counts.values)])
    fig.update_layout(title='Brand Preference (Private vs National)', xaxis_title='Brand Type', yaxis_title='Count')

    return fig.to_html(full_html=False)
