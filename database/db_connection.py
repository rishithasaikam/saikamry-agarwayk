from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Transaction(db.Model):
    __tablename__ = 'transactions'

    hshd_num = db.Column(db.String(20), primary_key=True)
    basket_num = db.Column(db.String(20), primary_key=True)
    purchase_ = db.Column(db.String(20))
    product_num = db.Column(db.String(20))
    spend = db.Column(db.Float)
    units = db.Column(db.Integer)
    store_r = db.Column(db.String(50))    # FIX: store_r, not store_region
    week_num = db.Column(db.Integer)
    year = db.Column(db.Integer)

class Product(db.Model):
    __tablename__ = 'products'

    product_num = db.Column('PRODUCT_NUM', db.String(50), primary_key=True)
    department = db.Column('DEPARTMENT', db.String(100))
    commodity = db.Column('COMMODITY', db.String(100))
    brand_ty = db.Column('BRAND_TY', db.String(50))
    natural_organic_flag = db.Column('NATURAL_ORGANIC_FLAG', db.String(50))


class Household(db.Model):
    __tablename__ = 'households'

    hshd_num = db.Column('HSHD_NUM', db.String(50), primary_key=True)
    l = db.Column('L', db.String(50))  # Loyalty flag
    age_range = db.Column('AGE_RANGE', db.String(50))
    marital = db.Column('MARITAL', db.String(50))
    income_range = db.Column('INCOME_RANGE', db.String(50))
    homeowner = db.Column('HOMEOWNER', db.String(50))
    hshd_composition = db.Column('HSHD_COMPOSITION', db.String(50))
    hh_size = db.Column('HH_SIZE', db.String(50))
    children = db.Column('CHILDREN', db.String(50))
