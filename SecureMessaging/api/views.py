import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from Service.models import Message, generate_random_string

# Create your views here.

MESSAGE_BAD_REQUEST_LIMIT = 8


@api_view(['GET'])
def get_message(request, message_id):
    try:
        message = Message.objects.get(message_id=message_id)
        if message.is_disposed:
            return JsonResponse({'error': 'Message is disposed'}, status=403)
        if request.GET.get('hash') != message.key_hash:
            message.number_of_bad_requests += 1
            if message.number_of_bad_requests >= MESSAGE_BAD_REQUEST_LIMIT:
                message.is_disposed = True
            message.save()
            return JsonResponse({'error': 'Invalid hash'}, status=403)
        if request.GET.get('hash') == message.key_hash:
            print(message.message)
            return JsonResponse(message.message, status=200, safe=False)
    except Message.DoesNotExist:
        return JsonResponse({'error': 'Message not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def create_message(request):
    try:
        data = json.loads(request.body)
        message = Message()
        message.message_id = generate_random_string(16)
        message.message = data.get('message')
        message.key_hash = data.get('hash')
        message.save()
        return JsonResponse({'status': "created", "details": {
            "message_id": message.message_id,
        }}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
