import sqlite3
from flask import Flask, escape, request, g, send_file
import config

app = Flask(__name__)

# Due to sqlite3/Flask threading issues, we need this semi-Singleton
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
    	# isolation_level=None means that all INSERTS/UPDATES
    	# take place immediately, no need to .commit() them.
        #db = g._database = sqlite3.connect(config.config['db_name'], isolation_level=None)
        db = g._database = sqlite3.connect(config.config['db_name'])

        # This allows us to get row results by name
        db.row_factory = sqlite3.Row
    return db

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return 'Hello, '+escape(name)+'!'

@app.route('/postman')
def postman():
    return send_file('./static/Postman.json', as_attachment=True)

@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()

import routes

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=8000)