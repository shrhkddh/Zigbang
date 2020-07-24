from django.urls import path

from map.views import (
    RoomListView,
    RoomDetailView,
    NearComplexInfoView
)

urlpatterns = [
    path('/complex/<int:code>', RoomListView.as_view()),
    path('/item/<int:code>', RoomDetailView.as_view()),
    path('/map', NearComplexInfoView.as_view())
]
