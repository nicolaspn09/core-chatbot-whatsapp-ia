import requests

url = "https://graph.facebook.com/v18.0/YOUR_PHONE_NUMBER_ID/messages"
headers = {
    "Authorization": "Bearer YOUR_ACCESS_TOKEN",
    "Content-Type": "application/json"
}
data = {
    "messaging_product": "whatsapp",
    "to": "RECIPIENT_PHONE_NUMBER",
    "type": "text",
    "text": {"body": "Olá, esta é uma mensagem automatizada!"}
}

response = requests.post(url, json=data, headers=headers)
print(response.json())