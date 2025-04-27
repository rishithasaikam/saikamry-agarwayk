# utils/basket_analysis_ml.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from database.db_connection import db, Transaction
import plotly.graph_objs as go

def run_cross_sell_analysis(target_product_num):
    """
    Predict purchase of target_product_num based on other products using Random Forest.
    """

    # 1. Load transaction data
    data = db.session.query(Transaction.hshd_num, Transaction.product_num).limit(50000).all()
    df = pd.DataFrame(data, columns=['hshd_num', 'product_num'])

    # 2. Create Basket Matrix
    basket = df.pivot_table(index='hshd_num', columns='product_num', aggfunc=lambda x: 1, fill_value=0)

    if target_product_num not in basket.columns:
        # Graceful fallback chart if product number is not found
        fig = go.Figure()
        fig.add_annotation(
            text=f"🚫 Product {target_product_num} not found in dataset!",
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=20, color="red"),
            x=0.5, y=0.5,
            align="center"
        )
        fig.update_layout(title="Cross-Selling Analysis - Error")
        return fig.to_html(full_html=False)

    # 3. Prepare Features and Label
    X = basket.drop(columns=[target_product_num])  # All products except target
    y = basket[target_product_num]                 # Target: whether customer bought the product

    # 4. Train Random Forest
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    # 5. Feature Importance
    importances = pd.Series(model.feature_importances_, index=X.columns)
    top_cross_selling = importances.nlargest(10)

    # 6. Plot
    fig = go.Figure([go.Bar(x=top_cross_selling.index.astype(str), y=top_cross_selling.values)])
    fig.update_layout(
        title=f"Top Cross-Sell Products for Target Product {target_product_num}",
        xaxis_title="Product Number",
        yaxis_title="Importance Score"
    )

    return fig.to_html(full_html=False)
