from flask import render_template, request, redirect, url_for, flash
from datetime import datetime
from utils.auth import login_required
from extensions import db
from models import Product


def register_product_routes(app):
    @app.route('/product/add', methods=['GET', 'POST'])
    @login_required
    def add_product():
        if request.method == 'POST':
            name = request.form.get('name')
            expiry_date_str = request.form.get('expiry_date')
            description = request.form.get('description')
            
            if not name or not expiry_date_str:
                flash('Название и срок годности обязательны', 'danger')
                return redirect(url_for('add_product'))
            
            try:
                expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d').date()
                new_product = Product(
                    name=name,
                    expiry_date=expiry_date,
                    description=description
                )
                db.session.add(new_product)
                db.session.commit()
                flash('Товар успешно добавлен', 'success')
                return redirect(url_for('dashboard'))
            except Exception:
                db.session.rollback()
                flash('Ошибка при добавлении товара', 'danger')
                return redirect(url_for('add_product'))
        
        return render_template('add_product.html')
    
    @app.route('/product/edit/<int:id>', methods=['GET', 'POST'])
    @login_required
    def edit_product(id):
        product = Product.query.get_or_404(id)
        
        if request.method == 'POST':
            product.name = request.form.get('name')
            expiry_date_str = request.form.get('expiry_date')
            product.description = request.form.get('description')
            
            if not product.name or not expiry_date_str:
                flash('Название и срок годности обязательны', 'danger')
                return redirect(url_for('edit_product', id=id))
            
            try:
                product.expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d').date()
                db.session.commit()
                flash('Товар успешно обновлен', 'success')
                return redirect(url_for('dashboard'))
            except Exception:
                db.session.rollback()
                flash('Ошибка при обновлении товара', 'danger')
                return redirect(url_for('edit_product', id=id))
        
        return render_template('edit_product.html', product=product)
    
    @app.route('/product/delete/<int:id>', methods=['POST'])
    @login_required
    def delete_product(id):
        product = Product.query.get_or_404(id)
        
        try:
            db.session.delete(product)
            db.session.commit()
            flash('Товар успешно удален', 'success')
        except Exception:
            db.session.rollback()
            flash('Ошибка при удалении товара', 'danger')
        
        return redirect(url_for('dashboard'))


