from django.urls import path

from .views import (
    SignUpView,
    SignInView,
    AuthSMSView,
    PhoneAuthorizationConfirmView,
    KakaoSignInView
)

urlpatterns = [
    path('/sign-up', SignUpView.as_view()),
    path('/sign-in', SignInView.as_view()),
    path('/phone-auth', AuthSMSView.as_view()),
    path('/phone-confirm', PhoneAuthorizationConfirmView.as_view()),
    path('/kakao', KakaoSignInView.as_view())
]
