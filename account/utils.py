import jwt
import json

from django.http import JsonResponse

from zigbang.settings import SECRET_KEY, ALGORITHM
from .models import User

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token        = request.headers.get('Authorization', None)
            payload      = jwt.decode(token, SECRET_KEY, algorithms = ALGORITHM)
            user         = User.objects.get(id = payload['user_id'])
            request.user = user
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message' : 'Invalid_token' }, status=400)
        except Account.DoesNotExist:
            return JsonResponse({'message' : 'Invalid_user'}, status=400)
        return func(self, request, *args, **kwargs)
    return wrapper

