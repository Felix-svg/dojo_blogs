from flask import Flask
from sqlalchemy import MetaData
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)

app.secret_key = "dsjkdfiwsnsdddfdjdssbohjoiaavg"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dojo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

metadata = MetaData()
db = SQLAlchemy(metadata=metadata)
migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)



