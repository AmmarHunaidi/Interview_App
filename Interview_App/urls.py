from django.contrib import admin
from django.urls import path , include
from rest_framework.routers import DefaultRouter
from .api import hello_view , AudioViewSet , AuthViewSet

audio_router = DefaultRouter()
audio_router.register(r'audio', AudioViewSet, basename='audio')

user_router = DefaultRouter()
user_router.register(r'', AuthViewSet, basename='auth')


urlpatterns = [
    # path('' , hello_view , name = "hello"),
    path('admin/', admin.site.urls),
    path('api/' , include(audio_router.urls)),
    path('auth/' , include(user_router.urls)),
    path("__debug__/", include("debug_toolbar.urls")),
]
