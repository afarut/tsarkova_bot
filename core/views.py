import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils.webhook import proceed_update
from asgiref.sync import async_to_sync


@csrf_exempt
def index(request):
    try:
        async_to_sync(proceed_update)(request)
    except Exception as e:
        print(e)
    return JsonResponse({})