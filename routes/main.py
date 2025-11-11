from flask import render_template, redirect, url_for, session
from utils.auth import login_required
from models import Product


def register_main_routes(app):
    @app.route('/')
    def index():
        if 'user_id' in session:
            return redirect(url_for('dashboard'))
        return redirect(url_for('login'))
    
    @app.route('/dashboard')
    @login_required
    def dashboard():
        from datetime import date
        products = Product.query.order_by(Product.expiry_date.asc()).all()
        today = date.today()
        return render_template('dashboard.html', products=products, today=today)


