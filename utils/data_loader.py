import pandas as pd
from database.db_connection import Transaction, Household, Product, db

def upload_csv(file, dataset):
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].str.strip()
    batch_size = 500
    counter = 0

    if dataset == 'transactions':
        for _, row in df.iterrows():
            existing = Transaction.query.filter_by(
                hshd_num=row['HSHD_NUM'],
                basket_num=row['BASKET_NUM']
            ).first()

            if not existing:
                transaction = Transaction(
                    hshd_num=row['HSHD_NUM'],
                    basket_num=row['BASKET_NUM'],
                    purchase_=row['PURCHASE_'],
                    product_num=row['PRODUCT_NUM'],
                    spend=row['SPEND'],
                    units=row['UNITS'],
                    store_r=row['STORE_R'],
                    week_num=row['WEEK_NUM'],
                    year=row['YEAR']
                )
                db.session.add(transaction)

            counter += 1
            if counter % batch_size == 0:
                db.session.commit()

        db.session.commit()


    elif dataset == 'products':

        for _, row in df.iterrows():

            existing = Product.query.filter_by(

                product_num=row['PRODUCT_NUM']

            ).first()

            if not existing:
                product = Product(

                    product_num=row['PRODUCT_NUM'],

                    department=row['DEPARTMENT'],

                    commodity=row['COMMODITY'],

                    brand_ty=row['BRAND_TY'],

                    natural_organic_flag=row['NATURAL_ORGANIC_FLAG']

                )

                db.session.add(product)

            counter += 1

            if counter % batch_size == 0:
                db.session.commit()

        db.session.commit()

    elif dataset == 'households':
        for _, row in df.iterrows():
            existing = Household.query.filter_by(
                hshd_num=row['HSHD_NUM']
            ).first()

            if not existing:
                household = Household(
                    hshd_num=row['HSHD_NUM'],
                    l=row['L'],
                    age_range=row['AGE_RANGE'],
                    marital=row['MARITAL'],
                    income_range=row['INCOME_RANGE'],
                    homeowner=row['HOMEOWNER'],
                    hshd_composition=row['HSHD_COMPOSITION'],
                    hh_size=row['HH_SIZE'],
                    children=row['CHILDREN']
                )
                db.session.add(household)

            counter += 1
            if counter % batch_size == 0:
                db.session.commit()

        db.session.commit()



from database.db_connection import Transaction, Product

def load_data(hshd_num):
    results = db.session.query(
        Transaction.hshd_num,
        Transaction.basket_num,
        Transaction.purchase_,
        Transaction.product_num,
        Product.department,
        Product.commodity
    ).join(Product, Transaction.product_num == Product.product_num)\
     .filter(Transaction.hshd_num == str(hshd_num)).all()

    return results

