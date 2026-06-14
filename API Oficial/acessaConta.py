import requests

def busca_informacao_conta_business():
    # Substitua pelos valores corretos
    whatsapp_business_account_id = "1718413995388700"
    access_token = 'REMOVED_FOR_GITHUB'

    url = f"https://graph.facebook.com/v21.0/{whatsapp_business_account_id}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)

    # Exibindo o status e o corpo da resposta
    print(f"Status Code: {response.status_code}")
    print("Response:")
    print(response.json())


def busca_informacao_servico():
    # Substitua pelos valores corretos
    whatsapp_business_account_id = "1718413995388700"
    access_token = 'REMOVED_FOR_GITHUB'

    url = f"https://graph.facebook.com/v21.0/{whatsapp_business_account_id}"
    params = {
        "fields": "id,name,message_templates,phone_numbers"
    }
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # Realizando a requisição GET
    response = requests.get(url, headers=headers, params=params)

    # Exibindo o status e o corpo da resposta
    print(f"Status Code: {response.status_code}")
    print("Response:")
    print(response.json())

busca_informacao_servico()