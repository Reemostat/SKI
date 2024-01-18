import json
import requests
from django.shortcuts import render
from SKIClient.utils import encrypt, decrypt
from cryptography.fernet import Fernet

from SKIClient.utils.decrypt import Helper

TOKEN = "a31c2ff90debf04cead036391d5e2cec4a957230"


def home(request):
    return render(request, 'home.html')


def send(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        key = request.POST.get('key')

        response = requests.post('http://127.0.0.1:8000/api/message/', data=json.dumps({
            "message": encrypt(text, key),
            "hash": Helper.calculate_hash(key)
        }), headers={
            "Authorization": f"Token {TOKEN}",
            "Content-Type": "application/json"
        })

        if response.status_code == 201:
            return render(request, 'send.html', {'message_id': response.json()['details']['message_id']})
    else:
        return render(request, 'send.html', {
            "key": Fernet.generate_key().decode('utf-8')
        })


def retrieve(request):
    if request.method == 'POST':
        message_id = request.POST.get('message_id')
        key = request.POST.get('key')
        hashval = Helper.calculate_hash(key)
        print(hashval)
        response = requests.get(f'http://127.0.0.1:8000/api/message/{message_id}/?hash={hashval}')
        if response.status_code == 200:
            data = decrypt(response.json(), key)
            return render(request, 'retrieve.html', {'message': data})
        else:
            return render(request, 'retrieve.html', {'message': response.json()['error']})
    return render(request, 'retrieve.html')
