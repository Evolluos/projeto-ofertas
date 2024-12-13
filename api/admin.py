from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilita CORS

import sqlite3

# Configuração do banco de dados SQLite
DATABASE = 'ofertas.db'

def init_db():
    """Inicializa o banco de dados."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ofertas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            preco REAL NOT NULL,
            url_imagem TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Inicializa o banco de dados ao iniciar o servidor
init_db()

@app.route('/')
def home():
    return "Bem-vindo à API de Gerenciamento de Ofertas! Use as rotas adequadas para interagir com o sistema.", 200

# Rota: Cadastrar oferta
@app.route('/cadastrar_oferta', methods=['POST'])
def cadastrar_oferta():
    dados = request.json
    titulo = dados.get('titulo')
    preco = dados.get('preco')
    url_imagem = dados.get('url_imagem')

    if not titulo or not preco or not url_imagem:
        return jsonify({'erro': 'Todos os campos (titulo, preco, url_imagem) são obrigatórios'}), 400

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO ofertas (titulo, preco, url_imagem)
        VALUES (?, ?, ?)
    ''', (titulo, preco, url_imagem))
    conn.commit()
    conn.close()

    return jsonify({'mensagem': 'Oferta cadastrada com sucesso'}), 201

# Rota: Listar ofertas
@app.route('/listar_ofertas', methods=['GET'])
def listar_ofertas():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM ofertas')
    ofertas = cursor.fetchall()
    conn.close()

    ofertas_formatadas = [
        {'id': oferta[0], 'titulo': oferta[1], 'preco': oferta[2], 'url_imagem': oferta[3]}
        for oferta in ofertas
    ]
    return jsonify(ofertas_formatadas), 200

# Rota: Deletar oferta
@app.route('/deletar_oferta/<int:id>', methods=['DELETE'])
def deletar_oferta(id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM ofertas WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return jsonify({'mensagem': 'Oferta deletada com sucesso'}), 200

if __name__ == '__main__':
    app.run(debug=True)
