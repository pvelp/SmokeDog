import requests
from bot.settings import settings

params = {'token': settings.prime_hill_token}


def test_connection():
    url = 'https://open-api.p-h.app/api/v2/ping'
    return requests.get(url, params)


def get_templates():
    url = 'https://open-api.p-h.app/api/v2/getTemplates'
    return requests.get(url, params)


def create_client():
    url = "https://open-api.p-h.app/api/v2/createClients"
    body = {
        "clients": [
            {
                "lastName": "Чехов",
                "firstName": "Антон",
                "patronymic": "Павлович",
                "birthday": "2020-01-01",
                "sex": "1",
                "email": "info@prime-hill.com",
                "phone": "79777121350",
                "templateId": 9588,
                "cardNumber": "1234",
                "cardBarcode": "1234",
                "comment": "Посещает только на закате",
                "parent": "12351",
                'tags': [
                    '3812'
                ]
            }
        ]
    }

    response = requests.post(url=url, params=params, json=body)

    if response.status_code == 200:
        response = response.json()["response"][0]
        result = 'https://form.p-h.app/plug/'+response['hash']
        return result
    return response


def get_all_clients():
    url = 'https://open-api.p-h.app/api/v2/getAllClients'
    return requests.get(url, params)

