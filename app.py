"""Flask App Project."""

from flask import Flask, jsonify
from flask_cors import cross_origin
app = Flask(__name__)


@app.route('/')
@cross_origin()
def index():
    """Return homepage."""
    json_data = {'Hello': 'World!'}
    return jsonify(json_data)


if __name__ == '__main__':
    app.run(debug=True)