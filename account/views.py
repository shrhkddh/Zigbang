import json
import bcrypt
import jwt
import re
import os
import sys
import hashlib
import hmac
import base64
import time
import requests
from random import randint

from django.http import (
    JsonResponse,
    HttpResponse
)
from django.core.validators import (
    validate_email,
    RegexValidator
)
from django.core.exceptions import ValidationError
from django.views import View

from zigbang.settings import (
    SECRET_KEY,
    ALGORITHM,
    SMS_SEND_PHONE_NUMBER,
    AUTH_ACCESS_KEY,
    AUTH_SECRET_KEY
)
from .models import (
    User,
    AuthSMS
)
from .utils import login_decorator

class SignUpView(View):
    def post(self, request):
        account_data       = json.loads(request.body)
        password_validator = RegexValidator(regex = "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}")
        random_number      = str(randint(1000,99999))
        try:
            email = account_data['email']
            validate_email(email)
            if not User.objects.filter(email = email).exists():
                password_validator(account_data['password'])
                password  = bcrypt.hashpw(account_data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                name      = "이용자" + random_number
                User(
                    email    = email,
                    password = password,
                    name     = name
                ).save()
                user  = User.objects.get(email = email)
                token = jwt.encode({"user_id" : user.id}, SECRET_KEY, algorithm = ALGORITHM).decode('utf-8')

                return JsonResponse({"token" : token}, status = 200)
            return JsonResponse({"message" : "EXISTING_EMAIL"}, status = 404)

        except ValidationError:
            return JsonResponse({"message" : "INVALID_EMAIL_OR_PWD"}, status = 400)
        except KeyError:
            return JsonResponse({"message" : "INVALID_KEY"}, status = 400)

class SignInView(View):
    def post(self, request):
        account_data = json.loads(request.body)
        try:
            email = account_data['email']
            validate_email(email)
            if User.objects.filter(email = account_data['email']).exists():
                user = User.objects.get(email = account_data['email'])
                if bcrypt.checkpw(account_data['password'].encode('utf-8'), user.password.encode('utf-8')):
                    token = jwt.encode({"user_id" : user.id}, SECRET_KEY, algorithm = ALGORITHM).decode('utf-8')
                    return JsonResponse({'token' : token}, status = 200)
                return JsonResponse({"message" : "UNAUTHORIZED_PASSWORD"}, status = 400)
            return JsonResponse({"message" : "UNAUTHORIZED_EMAIL"}, status = 400)
        except KeyError:
            return JsonResponse({"message" : "INVALID_KEY"}, status = 400)

class AuthSMSView(View):
    def sms_verification_send(self, phone_number, auth_number):
        SMS_URL    = "https://sens.apigw.ntruss.com/sms/v2/services/ncp:sms:kr:259801177571:smstest/messages"
        timestamp  = int(time.time() * 1000)
        timestamp  = str(timestamp)

        secret_key = bytes(AUTH_SECRET_KEY, 'utf-8')

        method     = "POST"
        uri        = "/sms/v2/services/ncp:sms:kr:259801177571:smstest/messages"

        message    = method + " " + uri + "\n" + timestamp + "\n" + AUTH_ACCESS_KEY
        message    = bytes(message, 'utf-8')
        signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod = hashlib.sha256).digest())

        headers = {
            'Content-Type'             : 'application/json; charset=utf-8',
            'x-ncp-apigw-timestamp'    : timestamp,
            'x-ncp-iam-access-key'     : 'a9vP5y6RE4IR6tOm4Qit',
            'x-ncp-apigw-signature-v2' : signingKey
        }
        messages = {"to" : phone_number}
        data = {
            'type'        : 'SMS',
            'contentType' : 'COMM',
            'countryCode' : '82',
            'from'        : f'{SMS_SEND_PHONE_NUMBER}',
            'messages'    : [messages],
            'content'     : f'인증번호 {auth_number}'
        }

        encoded_data = json.dumps(data)
        res          = requests.post(SMS_URL, headers = headers, data = encoded_data)
        return HttpResponse(status = res.status_code)

    @login_decorator
    def post(self, request):
        try:
            input_data          = json.loads(request.body)
            input_phone_number  = input_data['phone_number']
            created_auth_number = str(randint(1000, 9999))

            phone_number = AuthSMS.objects.update_or_create(phone_number = input_phone_number, defaults = {'phone_number' : input_phone_number, 'auth_number' : created_auth_number},)
            self.sms_verification_send(phone_number = input_phone_number, auth_number = created_auth_number)
            return HttpResponse(status = 200)
        except KeyError:
            return JsonResponse({"message":"INVALID_KEY"}, status = 400)

class PhoneAuthorizationConfirmView(View):
    @login_decorator
    def post(self, request):
        try:
            input_data                 = json.loads(request.body)
            user_account               = request.user
            input_phone_number         = input_data['phone_number']
            input_authorization_number = input_data['authorization_number']
            if input_authorization_number == AuthSMS.objects.get(phone_number = input_phone_number).auth_number:
                user_account.phone_number = AuthSMS.objects.get(phone_number = input_phone_number)
                user_account.save()
                return HttpResponse(status = 200)
            return JsonResponse({"message" : "INVALID_CODE"}, status = 400)
        except KeyError:
            return JsonResponse({"message" : "INVALID_KEY"}, status = 400)

class KakaoSignInView(View):
    def get(self, request):
        try:
            access_token    = request.headers.get('Authorization', None)
            profile_request = requests.get(
                'https://kapi.kakao.com/v2/user/me', 
                headers = {
                    'Authorization': f"Bearer {access_token}"
                }
            )
            profile    = profile_request.json()
            email      = profile.get('email',None)
            kakao_id   = profile.get('id', None)
            if kakao_id == None:
                return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)

            if User.objects.filter(social_login_id = kakao_id).exists():
                user  = User.objects.get(social_login_id = kakao_id)
                token = jwt.encode(
                    {'user_id': user.id}, 
                    SECRET_KEY, 
                    algorithm = ALGORITHM
                ).decode('utf-8')
                return JsonResponse({'token' : token}, status = 200)

            User.objects.create(
                email           = email,
                social_login_id = kakao_id
            )
            return HttpResponse(status = 200)
        except KeyError:
            return JsonResponse({'message': 'INVALID_KEY'}, status = 400)
