from flask import Flask, render_template, jsonify, request
import json
from formatador_dados import formatar_dados

app = Flask(__name__)

@app.route('/')
def home():
    with open('./dados_json/estados_sul_dados_integrados.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    data = formatar_dados(data)
    return render_template('index.html', dados=data)

if __name__ == '__main__':
    app.run(debug=True)
