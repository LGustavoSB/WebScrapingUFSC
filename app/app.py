from flask import Flask, render_template, jsonify, request
import json
from formatador_dados import formatar_dados

app = Flask(__name__)

@app.route('/')
def home():
    with open('./estados_sul_dados_integrados.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    data = formatar_dados(data)
    return render_template('index.html', dados=data)

@app.route('/api/dados')
def dados():
    with open('../estados_sul_IBGE.json') as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/api/processar', methods=['POST'])
def processar():
    req_data = request.json
    resposta = {"mensagem": f"Recebido com sucesso: {req_data}"}
    return jsonify(resposta)

if __name__ == '__main__':
    app.run(debug=True)
