import flask
from flask import jsonify
import requests

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route("/", methods=['GET'])
def index():
    response = requests.get('https://randomuser.me/api')
    return jsonify(response.json())  # Correção aqui

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
