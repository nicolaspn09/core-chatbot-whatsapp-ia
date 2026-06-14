from flask import Flask, request, jsonify
from services.waha import Waha
from bot.ai_bot import AIBot
import time
import random
import datetime
import os

app = Flask(__name__)

@app.route("/chatbot/webhook/", methods=["POST"])

def webhook():
    data = request.json

    print(f"EVENTO RECEBIDO: {data}")

    # Inicializa a classe
    waha = Waha()

    # Inicializa o bot
    bot = AIBot()

    # Obtém o ID do chat
    chat_id = data["payload"]["from"]

    # Obtém a mensagem do usuário
    received_message = data["payload"]["body"]

    # Pessoa que enviou a mensagem
    notify_name = data["payload"]["_data"]["notifyName"]

    # Busca a data de hora da mensagem
    timestamp = data["payload"]["timestamp"]

    # Converte o timestamp para datetime em UTC
    dt_utc = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)
    # print(f"Timestamp convertido para UTC: {dt_utc}")

    # Obtém a hora atual em UTC-3 (ajustando automaticamente para o fuso horário São Paulo)
    now_utc_minus_3 = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-3)))
    # print(f"Hora atual em UTC-3: {now_utc_minus_3}")

    # Calcula a diferença de tempo entre agora (UTC-3) e o timestamp ajustado
    time_difference = now_utc_minus_3 - dt_utc
    # print(f"Diferença de tempo entre a mensagem e o momento atual: {time_difference}")

    # Verifica se a diferença é menor que 1 hora
    if time_difference < datetime.timedelta(hours=1):
        # Verifica se é grupo
        is_group = "@g.us" in chat_id
        is_status = "status@broadcast" in chat_id

        # Inicia a simulação de resposta
        waha.start_typing(chat_id=chat_id)

        # Gera um tempo randômico
        time.sleep(random.randint(3, 15))

        # Pega o histórico de conversação
        history_message = waha.get_history_messages(chat_id=chat_id, limit=10)
        
        # Busca o histórico das mensagens
        # received_message = f"Contexto das mensagens anteriores: {history_message}. Mensagem recebida agora: {received_message}"
        
        # Busca a resposta da IA
        response = bot.invoke(history_messages=history_message, question=received_message)

        # Finaliza a simulação de estar digitando
        waha.stop_typing(chat_id=chat_id)

        # Envia a mensagem
        waha.send_message(
            chat_id=chat_id,
            message=f"{response}"
        )

        return jsonify({"status": "success"}), 200
    
    else:
        return jsonify({"status": "message_too_old"}), 400

if __name__ == "__main__":
     app.run(host = 'REMOVED', port=int(os.environ.get("PORT", 5000)), debug=True)
