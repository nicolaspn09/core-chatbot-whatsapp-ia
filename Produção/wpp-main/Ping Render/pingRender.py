import requests
import time

# URL do serviço que você deseja manter ativo no Render
url = "https://api-fp9b.onrender.com"  # Substitua pela URL do seu serviço

url2 = "https://waha-zirw.onrender.com"

# Intervalo entre os pings (em segundos)
ping_interval = 30  # 300 segundos = 5 minutos

def send_ping(url):
    try:
        # Envia uma requisição GET para o serviço
        response = requests.get(url)
        
        # Verifica se a requisição foi bem-sucedida
        if response.status_code == 200:
            print(f"Ping bem-sucedido para {url}!")
        else:
            print(f"Erro ao fazer ping no serviço. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer requisição: {e}")

def send_ping_waha(url):
    try:
        # Envia uma requisição GET para o serviço
        response = requests.get(url)
        
        # Verifica se a requisição foi bem-sucedida
        if response.status_code == 200:
            print(f"Ping bem-sucedido para {url}!")
        else:
            print(f"Erro ao fazer ping no serviço. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer requisição: {e}")

if __name__ == "__main__":
    while True:
        send_ping(url=url)  # Envia o ping
        send_ping_waha(url=url2)  # Envia o ping
        time.sleep(ping_interval)  # Aguarda o intervalo de tempo (5 minutos)