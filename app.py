from flask import Blueprint, Flask, jsonify, request
from flask_cors import CORS

from blueprints.formula import formula_blueprints
from blueprints.input_variable import input_variable_blueprints

app = Flask(__name__)
CORS(app)

app.register_blueprint(formula_blueprints, url_prefix="/formula")
app.register_blueprint(input_variable_blueprints, url_prefix="/input_variable")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=4666)
