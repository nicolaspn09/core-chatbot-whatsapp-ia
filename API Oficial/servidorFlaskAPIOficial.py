from flask import Flask, request, jsonify

app = Flask(__name__)

# Token de verificação (deve ser o mesmo configurado no painel do Facebook)
VERIFY_TOKEN = 'REMOVED_FOR_GITHUB'

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Verificar se o token de verificação corresponde ao que o Facebook enviou
        verify_token = request.args.get('hub.verify_token')
        if verify_token == 'meu_token_123':
            # Se o token for válido, enviar o desafio de volta
            return request.args.get('hub.challenge'), 200
        else:
            return 'Error, invalid token', 403  # Token inválido
    else:
        # Quando o método for POST, você pode processar os dados enviados
        data = request.get_json()
        print("Dados recebidos:", data)
        return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    # Rodar o servidor na porta 5000
    app.run(host = 'REMOVED', port=5000)