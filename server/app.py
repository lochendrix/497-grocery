from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_login import current_user
from extensions import db, login_manager
from routes.auth import auth_bp  # Authentication routes blueprint (create this file)
import os
import json

from services.kroger import *
from services.usda import *

from parsers_and_integration import *

from grocery_data_frontend_algs import *

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
        store_count, store_list = Kroger_get_store_list("48109")
        store_info = Kroger_parse_stores_list(store_list)
        

        grocery_list_obj = Kroger_get_grocery_list(store_info["ID"], "Protein")
        grocery_list_obj.full_preparation()
        output = grocery_list_obj.prep_JSON_for_webpage()

        with open("static/grocery_list.json", "w") as f:
            f.write(json.dumps(output, indent=4))

        # For mockup purposes, just return the string
        return render_template('index.html')

    @app.route('/submit', methods=['POST'])
    def submit():
        # Get the JSON data sent from the frontend
        data = request.get_json()
        text = data.get('text', '')
        
        print(text)
        
        return render_template('index.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
