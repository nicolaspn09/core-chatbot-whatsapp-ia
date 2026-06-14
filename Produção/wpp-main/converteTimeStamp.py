import datetime

# Timestamp fornecido
timestamp = 1732824472

# Converte o timestamp para datetime em UTC
dt_utc = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)

# Ajusta para UTC-3
dt_utc_minus_3 = dt_utc - datetime.timedelta(hours=3)

# Obtém a data e hora atual no horário UTC-3
now_utc_minus_3 = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-3)))

# Calcula a diferença de tempo entre agora e o timestamp fornecido
time_difference = now_utc_minus_3 - dt_utc_minus_3

# Verifica se a diferença é menor do que 1 hora
if time_difference < datetime.timedelta(hours=1):
    print("O horário fornecido está a menos de 1 hora de distância da hora atual.")
else:
    print("O horário fornecido está a mais de 1 hora de distância da hora atual.")