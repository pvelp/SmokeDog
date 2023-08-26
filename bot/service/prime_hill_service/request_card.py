import requests
from bot.settings import settings
from bot.core.models import PrimeHillModel

params = {'token': settings.prime_hill_token}


def test_connection():
    url = 'https://open-api.p-h.app/api/v2/ping'
    return requests.get(url, params)


def get_templates():
    url = 'https://open-api.p-h.app/api/v2/getTemplates'
    return requests.get(url, params)


def create_client(client: PrimeHillModel):
    # client.json()
    url = "https://open-api.p-h.app/api/v2/createClients"
    body = {
        "clients": [
            {
                "lastName": client.lastName,
                "firstName": client.firstName,
                "patronymic": client.patronymic,
                "birthday": client.birthday,
                "sex": client.sex,
                "email": client.email,
                "phone": client.phone,
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

