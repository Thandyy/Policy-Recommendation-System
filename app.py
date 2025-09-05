from views.admin import admin_bp
from views.client import client_bp
from views.authentication import authentication_bp
from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)



app.register_blueprint(admin_bp)
app.register_blueprint(client_bp)
app.register_blueprint(authentication_bp)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'authentication.login'


# running the application @ port 5000
if __name__ == '__main__':
    app.run(debug=True, port=5000)