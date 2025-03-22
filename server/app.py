from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

# Import the Kroger service function
from services.kroger import get_store_info

@app.route('/kroger')
def kroger():
    # Call the Kroger API code and get the result string
    store_info = get_store_info()
    # For mockup purposes, just return the string
    return f"<pre>{store_info}</pre>"

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)