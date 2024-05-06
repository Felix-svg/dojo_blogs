from flask import Flask
from sqlalchemy import MetaData
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_jwt_extended import JWTManager

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)

#app.secret_key = "dsjkdfiwsnsdddfdjdssbohjoiaavg"
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dojo.db"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://my_database_c7w2_user:z2gVEkzO4wQMKw3rtMq6F8MHUTbPcMPN@dpg-coka46ud3nmc7396q1mg-a.oregon-postgres.render.com/dojo_blogs_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['JWT_SECRET_KEY'] = 'dsjkdfiwsnsdddfdjdssbohjoiaavg'
app.json.compact = False

metadata = MetaData()
db = SQLAlchemy(metadata=metadata)
migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

jwt = JWTManager(app)


