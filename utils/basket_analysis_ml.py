# utils/basket_analysis_ml.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from database.db_connection import db, Transaction
import plotly.graph_objs as go

def run_cross_sell_analysis(target_product_num):
    """
    Predict purchase of target_product_num based on other products using Random Forest
    """

    # 1. Load transaction data
    data = db.session.query(Transaction.hshd_num, Transaction.product_num).all()
    df = pd.DataFrame(data, columns=['hshd_num', 'product_num'])

    # 2. Create Basket Matrix
    basket = df.pivot_table(index='hshd_num', columns='product_num', aggfunc=lambda x: 1, fill_value=0)

    # 3. Check if target product exists
    if target_product_num not in basket.columns:
        fig = go.Figure()
        fig.add_annotation(
            text=f"Product Number {target_product_num} not found in transactions!",
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=18, color="red")
        )
        fig.update_layout(title="Cross-Sell Analysis Error")
        return fig.to_html(full_html=False)

    # 4. Prepare Features and Label
    X = basket.drop(columns=[target_product_num])
    y = basket[target_product_num]

    # 5. Train Random Forest
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    # 6. Feature Importance
    importances = pd.Series(model.feature_importances_, index=X.columns)
    top_cross_selling = importances.nlargest(10)

    # 7. Plot
    fig = go.Figure([go.Bar(x=top_cross_selling.index.astype(str), y=top_cross_selling.values)])
    fig.update_layout(
        title=f"Top Cross-Sell Products for Target Product {target_product_num}",
        xaxis_title="Product Number",
        yaxis_title="Importance Score"
    )

    return fig.to_html(full_html=False)
