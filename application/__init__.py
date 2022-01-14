from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)

from application.main import bp as main_bp
app.register_blueprint(main_bp)

from application import models