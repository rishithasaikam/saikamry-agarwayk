import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

df = pd.read_csv("data/400_transactions.csv")
basket = df.groupby(['basket_num', 'product_num'])['units'].sum().unstack().fillna(0)
basket = basket.applymap(lambda x: 1 if x > 0 else 0)

frequent_itemsets = apriori(basket, min_support=0.01, use_colnames=True)
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)

print(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']])
