# app.py

from flask import Flask, render_template, request, redirect, url_for, session, flash
from utils.data_loader import load_data, upload_csv
from utils.model_helpers import predict_clv, predict_churn, analyze_basket
from utils.dashboard_charts import plot_spend_over_time, plot_brand_preference
from database.db_connection import db, User, Transaction, Product, Household
from config import DATABASE_URI, SECRET_KEY
from utils.basket_analysis_ml import run_cross_sell_analysis
import os
from utils.dashboard_charts import (
    plot_spend_over_time,
    plot_brand_preference,
    plot_top_categories_over_time
)

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please log in.', 'danger')
            return redirect(url_for('login'))
        new_user = User(email=email, username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Signup successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        print(f"DEBUG: user found = {user}")  # ADD THIS LINE

        if user and user.password == password:
            print("DEBUG: Password matches!")  # ADD THIS LINE
            session.clear()
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            print("DEBUG: Login failed.")  # ADD THIS LINE
            flash('Invalid email or password', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')



@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('landing'))

from utils.model_helpers import predict_clv, predict_churn, analyze_basket
from utils.dashboard_charts import plot_spend_over_time, plot_brand_preference

@app.route('/dashboard')
def dashboard():
    clv_fig = predict_clv()
    churn_fig = predict_churn()
    basket_fig = analyze_basket()
    spend_time_fig = plot_spend_over_time()
    brand_pref_fig = plot_brand_preference()
    top_cat_fig = plot_top_categories_over_time()

    return render_template('dashboard.html',
                           clv_fig=clv_fig,
                           churn_fig=churn_fig,
                           basket_fig=basket_fig,
                           spend_time_fig=spend_time_fig,
                           brand_pref_fig=brand_pref_fig,
                           top_cat_fig=top_cat_fig)

@app.route('/cross_sell', methods=['GET', 'POST'])
def cross_sell():
    cross_sell_fig = None

    if request.method == 'POST':
        target_product_num = int(request.form['target_product_num'])
        cross_sell_fig = run_cross_sell_analysis(target_product_num)

    return render_template('cross_sell.html', cross_sell_fig=cross_sell_fig)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    success = None
    if request.method == 'POST':
        file = request.files['file']
        dataset = request.form['dataset']

        # Just upload the file (upload_csv should NOT return redirect)
        upload_csv(file, dataset)

        # After upload, stay on page and show success message
        success = "File uploaded successfully!"

    return render_template('upload.html', success=success)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    results = None
    if request.method == 'POST':
        hshd_num = request.form['hshd_num'].strip()
        if hshd_num:
            results = load_data(hshd_num)
            print(f"DEBUG: Searching for HSHD_NUM = {hshd_num}, Results = {len(results)}")
        else:
            flash('Please enter a valid HSHD_NUM.', 'danger')
            return redirect(url_for('search'))

    return render_template('search.html', results=results)
if __name__ == '__main__':
    app.run(debug=True)
