from django.urls import path, include

urlpatterns = [
    path('studio-flat', include('map.urls')),
    path('account', include('account.urls')),
    path('search', include('search.urls')),
]
