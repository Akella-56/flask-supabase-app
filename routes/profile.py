from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash
from utils.auth import login_required
from extensions import db
from models import User


def register_profile_routes(app):
    @app.route('/profile', methods=['GET', 'POST'])
    @login_required
    def profile():
        user = User.query.get_or_404(session['user_id'])
        
        if request.method == 'POST':
            name = request.form.get('name')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            
            if not name:
                flash('Имя не может быть пустым', 'danger')
                return redirect(url_for('profile'))
            
            user.name = name
            session['user_name'] = name
            
            if password or confirm_password:
                if password != confirm_password:
                    flash('Пароли не совпадают', 'danger')
                    return redirect(url_for('profile'))
                user.password = generate_password_hash(password)
            
            try:
                db.session.commit()
                flash('Профиль обновлен', 'success')
            except Exception:
                db.session.rollback()
                flash('Ошибка при обновлении профиля', 'danger')
            
            return redirect(url_for('profile'))
        
        return render_template('profile.html', user=user)


