from flask import Flask
from flaskServer.models import db, db_url

app = Flask(__name__, template_folder='/apolloShield/flaskServer/public', static_folder='/apolloShield/flaskServer/public')

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

db.init_app(app)

from flaskServer import routes

#if __name__ == "__main__":
#	app.run(host='0.0.0.0', port='8055')
