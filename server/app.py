from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    # Import and register blueprints inside the factory
    from routes.api import api
    app.register_blueprint(api, url_prefix='/api')

    @app.route('/')
    def index():
        return "Backend is up and running!"
        
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)