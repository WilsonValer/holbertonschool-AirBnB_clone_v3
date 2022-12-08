#!/usr/bin/python3
''' Return the status of an API '''
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv  # to use environmental variables
from flask import jsonify
from werkzeug.exceptions import HTTPException  # to use errorhandler


# instance app variable from Flask class
app = Flask(__name__)
# register the blueprint app_views for use
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    ''' Remove the current SQLAlchemy Session '''
    storage.close()


@app.errorhandler(HTTPException)
def handle_exception(error):
    ''' Use errorhandler to display 404 error page '''
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    # return env variable if it exists
    # otherwise return second argument
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True, debug=True)
