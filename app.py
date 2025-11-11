import os
import re
import urllib.parse
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime
from extensions import db
from routes.auth import register_auth_routes
from routes.main import register_main_routes
from routes.products import register_product_routes
from routes.profile import register_profile_routes

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')

db_uri = os.environ.get('SUPABASE_POOLER_URL', '')
if db_uri:
    if db_uri.startswith('postgres://'):
        db_uri = db_uri.replace('postgres://', 'postgresql://', 1)
    
    match = re.match(r'(postgresql://[^:]+):([^@]+)@(.+)', db_uri)
    if match:
        prefix, password, rest = match.groups()
        if any(c in password for c in ['@', ':', '/', '?', '#', '[', ']', '!', '$', '&', "'", '(', ')', '*', '+', ',', ';', '=']):
            encoded_password = urllib.parse.quote(password, safe='')
            db_uri = f"{prefix}:{encoded_password}@{rest}"

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}

db.init_app(app)

from models import User, Product  # noqa: E402
from utils.auth import login_required  # noqa: E402

# Создание таблиц при первом запуске
with app.app_context():
    db.create_all()

# Регистрация маршрутов из модулей
register_auth_routes(app)
register_main_routes(app)
register_product_routes(app)
register_profile_routes(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

# gsdfg

