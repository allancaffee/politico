from flask import Flask, render_template, jsonify
from flask.ext.bootstrap import Bootstrap
from flask.ext.restless import APIManager

from politico.api import api
from politico.model import make_conn_str, db, Messages


app = Flask(__name__)

app.config_obj = {}

# Note, this url namespace also exists for the Flask-Restless
# extension and is where CRUD interfaces live, so be careful not to
# collide with model names here. We could change this, but it's nice
# to have API live in the same url namespace.
app.register_blueprint(api, url_prefix='/api')

manager = APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(Messages, methods=['GET', 'POST'])


Bootstrap(app)


def init_webapp():
  app.config['SQLALCHEMY_DATABASE_URI'] = make_conn_str()
  db.app = app
  db.init_app(app)
  db.create_all()
  return app


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/state/<state>', methods=['GET'])
def state(state):
  return jsonify({'state': state})
