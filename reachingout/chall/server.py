from flask import Flask
from endpoints import home

app = Flask(__name__)

# Register blueprints
app.register_blueprint(home.bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
