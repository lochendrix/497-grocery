from flask import Flask, render_template, redirect, url_for
from flask_login import current_user
from extensions import db, login_manager
from services.kroger import get_store_info
from routes.auth import auth_bp  # Authentication routes blueprint (create this file)
import os

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.config['SECRET_KEY'] = 'make this more secure later' 

    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    from models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import blueprints or routes after creating the app
    app.register_blueprint(auth_bp)

    @app.route('/')
    def index():
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        return render_template('index.html')
    
    @app.route('/kroger')
    def kroger():
        # Call the Kroger API code and get the result string
        store_info = get_store_info()
        # For mockup purposes, just return the string
        return f"<pre>{store_info}</pre>"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
