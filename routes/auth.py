from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from models import User


def register_auth_routes(app):
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            
            if not name or not email or not password:
                flash('Все поля обязательны для заполнения', 'danger')
                return redirect(url_for('register'))
            
            if password != confirm_password:
                flash('Пароли не совпадают', 'danger')
                return redirect(url_for('register'))
            
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('Пользователь с такой почтой уже существует', 'danger')
                return redirect(url_for('register'))
            
            hashed_password = generate_password_hash(password)
            new_user = User(name=name, email=email, password=hashed_password)
            
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Регистрация успешна! Теперь вы можете войти', 'success')
                return redirect(url_for('login'))
            except Exception:
                db.session.rollback()
                flash('Произошла ошибка при регистрации', 'danger')
                return redirect(url_for('register'))
        
        return render_template('register.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            
            if not email or not password:
                flash('Заполните все поля', 'danger')
                return redirect(url_for('login'))
            
            user = User.query.filter_by(email=email).first()
            
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                session['user_name'] = user.name
                flash(f'Добро пожаловать, {user.name}!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Неверная почта или пароль', 'danger')
                return redirect(url_for('login'))
        
        return render_template('login.html')
    
    @app.route('/logout')
    def logout():
        session.clear()
        flash('Вы успешно вышли из системы', 'info')
        return redirect(url_for('login'))


