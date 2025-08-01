import flask
from flask import jsonify
import requests
from flask_mysqldb import MySQL  # Corrigido o import

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config["MYSQL_HOST"] = 'host.docker.internal'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'flaskhost'

mysql = MySQL(app)  # Instancia o objeto MySQL com o app Flask

@app.route("/", methods=['GET'])
def index():
    response = requests.get('https://randomuser.me/api')
    return jsonify(response.json())

@app.route("/inserthost", methods=['POST'])
def inserthost():
    # Correção: chamar requests.get e não requests diretamente
    data = requests.get('https://randomuser.me/api').json()
    username = data['results'][0]['name']['first']

    cur = mysql.connection.cursor()
    # Adiciona vírgula extra para garantir que `username` seja interpretado como tupla
    cur.execute("INSERT INTO users(name) VALUES(%s)", (username,))
    mysql.connection.commit()  # Salva a transação
    cur.close()

    return jsonify({"inserted_name": username})

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
