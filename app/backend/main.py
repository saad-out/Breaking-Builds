from flask import Flask
from dotenv import load_dotenv
from os import environ

from jenkins_api import server
from routes import routes_bp

load_dotenv()

app = Flask(__name__)
app.secret_key = environ.get('APP_SECRET_KEY')
app.url_map.strict_slashes = False
app.register_blueprint(routes_bp)

@app.route('/')
def hello_world():
    return 'Hello, World!!!'

if __name__ == "__main__":
    app.run(
        host=environ.get('APP_HOST', '0.0.0.0'),
        port=int(environ.get('APP_PORT', 5000)),
        debug=bool(environ.get('APP_DEBUG', False))
    )
