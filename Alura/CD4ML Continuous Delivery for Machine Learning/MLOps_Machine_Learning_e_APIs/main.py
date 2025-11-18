from flask import Flask
from textblob import TextBlob

app = Flask(__name__)

@app.route('/')
def home():
    return 'Minha primeira API.'

@app.route('/sentimento/<frase>')
def sentimento(frase):
    tb = TextBlob(frase)
    tb_en = tb.translate(from_lang='pt', to='en')
    polaridade = tb_en.sentiment.polarity
    return f"polaridade:{polaridade}"

if __name__ == '__main__':
    print("Acessar o servidor em http://localhost:8000")
    app.run(
        host='0.0.0.0',  # Permite acesso de outros dispositivos na rede
        port=8000,
        debug=True
    )