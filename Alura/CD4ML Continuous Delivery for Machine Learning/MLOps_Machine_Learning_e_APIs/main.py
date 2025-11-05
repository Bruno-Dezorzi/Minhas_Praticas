from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Minha primeira API.'

if __name__ == '__main__':
    print("Acessar o servidor em http://localhost:8000")
    app.run(
        host='0.0.0.0',  # Permite acesso de outros dispositivos na rede
        port=8000,
        debug=True
    )