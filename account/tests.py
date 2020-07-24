import json
import bcrypt
import jwt

from unittest.mock import (
    patch,
    MagicMock,
    Mock
)
from django.test import (
    TestCase,
    Client
)

from zigbang.settings import (
    SECRET_KEY,
    ALGORITHM,
    TOKEN_FOR_UNIT_TEST
)
from .models import (
    User,
    AuthSMS
)
from django.http import HttpResponse

class SignUpTest(TestCase):
    def setUp(self):
        password = bcrypt.hashpw("abcd1234".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        User.objects.create(
            email    = "abc123@gmail.com",
            password = password
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_signup_post_success(self):
        client = Client()
        user = {
                'email'    : 'bca321@gmail.com',
                'password' : 'dcba4321'  
        }

        response = client.post('/account/sign-up', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_signup_post_duplicated_email(self):
        client = Client()
        user = {'email'    : 'abc123@gmail.com',
                'password' : 'abcd1234'
        }
        response = client.post('/account/sign-up', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), 
            {
                "message" : "EXISTING_EMAIL"
            }
        )

    def test_signup_post_invalid_email(self):
        client = Client()
        user = {
                'email'    : 'zzzz',
                'password' : 'abcd1234'
        }
        response = client.post('/account/sign-up', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                {
                    "message" : "INVALID_EMAIL_OR_PWD"
                }
        )

    def test_signup_post_invalid_pwd(self):
        client = Client()
        user = {
                'email'    : 'zxc123@gmail.com',
                'password' : '!!!'
        }
        response = client.post('/account/sign-up', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                {
                    "message" : "INVALID_EMAIL_OR_PWD" 
                }
        )
    def test_signup_post_invalid_keys(self):
        client = Client()
        user = {
                'email_hi' : 'bca321@gmail.com',
                'password' : 'dcba4321'  
        }
        response = client.post('/account/sign-up', json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
                {
                    "message" : "INVALID_KEY"
                }
        )
class SigninTest(TestCase):

    def setUp(self):
        password = bcrypt.hashpw("abcd1234".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        User.objects.create(
                id      = 1,
               email    = "abc123@gmail.com",
               password = password
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_signin_post_success(self):
        client = Client()
        user= { 'id'       : 1,
                'email'    : "abc123@gmail.com",
                'password' : "abcd1234"
        }
        user1 = User.objects.get(id=1)
        token = jwt.encode({"user_id":user1.id}, SECRET_KEY, algorithm=ALGORITHM).decode('utf-8')
        response = client.post('/account/sign-in', json.dumps(user), content_type = 'application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'token':token}) 

    def test_signin_post_unauthorized_email(self):
        client = Client()
        user = {
                "email"    : "abcd123@gmail.com",
                "password" : "abcd1234"
        }
        response = client.post('/account/sign-in', json.dumps(user), content_type = 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message":"UNAUTHORIZED_EMAIL"})

    def test_signin_post_unauthorized_pwd(self):
        client = Client()
        user = {
                "email"    : "abc123@gmail.com",
                "password" : "abcde12345"
        }
        response = client.post('/account/sign-in', json.dumps(user), content_type = 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message" : "UNAUTHORIZED_PASSWORD"})

    def test_signin_post_invalid_keys(self):
        client = Client()
        user = {
                "amail"    : "abc123@gmail.com",
                "password" : "abcd1234"
        }
        response = client.post('/account/sign-in', json.dumps(user), content_type = 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message":"INVALID_KEY"})

class KakaoSigninTest(TestCase):

    def setUp(self):
        User.objects.create(id=1, social_login_id=12345, name="makao")

    def tearDown(self):
        User.objects.all().delete()

    def test_kakao_signin_success(self):
        with patch('account.views.requests.get') as mocked_get:

            class UserInfo:
                def json(self):
                    user_info = {
                        'id'            : '12345',
                        'properties'    : {
                            'nickname'        : 'test_user', 
                            'thumbnail_image' : 'https://interactive-examples.mdn.mozilla.net/media/examples/grapefruit-slice-332-332.jpg'},
                        'kakao_account' : {'email' : 'test@email.com'}
                    }
                    return user_info
            profile_request = UserInfo()
            mocked_get.return_value = profile_request


            client   = Client()
            response = client.get('/account/kakao')
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.json()['token'])

    def test_kakao_signin_singup(self):
        with patch('account.views.requests.get') as mocked_get:

            class UserInfo:
                def json(self):
                    user_info = {
                        'id'            : "54321",
                        'properties'    : {
                            'nickname'        : 'test_user', 
                            'thumbnail_image' : 'https://interactive-examples.mdn.mozilla.net/media/examples/grapefruit-slice-332-332.jpg'},
                        'kakao_account' : {'email': 'test@email.com'}
                    }
                    return user_info
            profile_request = UserInfo()
            mocked_get.return_value = profile_request

            client   = Client()
            response = client.get('/account/kakao')
            self.assertEqual(response.status_code, 200)

    def test_kakao_signin_invalid_keys(self):
        with patch('account.views.requests.get') as mocked_get:

            class UserInfo:
                def json(self):
                    user_info = {
                        'disdf'            : "54321",
                        'propertiesi'    : {
                            'nicknamei'       : 'test_user', 
                            'thumbnail_imagea' : 'https://interactive-examples.mdn.mozilla.net/media/examples/grapefruit-slice-332-332.jpg'},
                        'kakao_accounta' : {'emaili': 'test@email.com'}
                    }
                    return user_info
            profile_request = UserInfo()
            mocked_get.return_value = profile_request

            client   = Client()
            response = client.get('/account/kakao')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json(), {"message": "INVALID_KEY"})

class AuthSMSViewTest(TestCase):

    def setUp(self):
        User.objects.create(id=1, email="kpl5672@gmail.com", password="abcd1234")
        AuthSMS.objects.create(id=1, phone_number = "010-5552-5672", auth_number=1111)

    def tearDown(self):
        AuthSMS.objects.all().delete()

    @patch('account.views.requests')
    def test_sms_send_success(self, mocked_post):
        mocked_post.post = MagicMock(return_value = HttpResponse(status=202))
        client      = Client()
        user_info   = {"phone_number":"01055525672"}
        user_email  = User.objects.get(email='kpl5672@gmail.com').id
        token       = jwt.encode({'user_id' : user_email}, SECRET_KEY, algorithm=ALGORITHM).decode('utf-8')
        header      = {"HTTP_Authorization" : token}
        response    = client.post('/account/phone-auth', json.dumps(user_info),  **header, content_type = 'application/json')
        self.assertEqual(response.status_code, 200)

    @patch('account.views.requests')
    def test_sms_send_invalid_keys(self, mocked_post):
        mocked_post.post = MagicMock(return_value = HttpResponse(status=202))
        client      = Client()
        user_info   = {"phone_numbe":"01055525672"}
        user_email  = User.objects.get(email='kpl5672@gmail.com').id
        token       = jwt.encode({'user_id' : user_email}, SECRET_KEY, algorithm=ALGORITHM).decode('utf-8')
        header      = {"HTTP_Authorization" : token}
        response = client.post('/account/phone-auth', json.dumps(user_info), **header, content_type = 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'INVALID_KEY'})

class PhoneAuthorizationConfirmTest(TestCase):

    def setUp(self):
        User.objects.create(id=1, email="kpl5672@gmail.com", password="abcd1234")
        AuthSMS.objects.create(id=1, phone_number = "01055525672", auth_number="1111")

    def tearDown(self):
        User.objects.all().delete()
        AuthSMS.objects.all().delete()

    def test_phone_confirm_success(self):
        client     = Client()
        user_info  = {"phone_number":"01055525672", "authorization_number":"1111"}
        user_email = User.objects.get(email='kpl5672@gmail.com').id
        token      = jwt.encode({'user_id' : user_email}, SECRET_KEY, algorithm=ALGORITHM).decode('utf-8')
        header     = {"HTTP_Authorization" : token}
        response   = client.post('/account/phone-confirm', json.dumps(user_info), **header, content_type = 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_phone_confirm_invalid_code(self):
        client     = Client()
        user_info  = {"phone_number":"01055525672", "authorization_number":"1113"}
        user_email = User.objects.get(email='kpl5672@gmail.com').id
        token      = jwt.encode({'user_id' : user_email}, SECRET_KEY, algorithm=ALGORITHM).decode('utf-8')
        header     = {"HTTP_Authorization" : token}
        response   = client.post('/account/phone-confirm', json.dumps(user_info), **header, content_type = 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'INVALID_CODE'})

    def test_phone_confirm_invalid_key(self):
        client     = Client()
        user_info  = {"p_number":"01055525672", "authorization_number":"1111"}
        user_email = User.objects.get(email='kpl5672@gmail.com').id
        token      = jwt.encode({'user_id' : user_email}, SECRET_KEY, algorithm=ALGORITHM).decode('utf-8')
        header     = {"HTTP_Authorization" : token}
        response   = client.post('/account/phone-confirm', json.dumps(user_info), **header, content_type = 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'INVALID_KEY'})
