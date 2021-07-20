from django.urls import path
from . import views

urlpatterns = [
    path('', views.wall),
    path('post_message', views.post_message),
    path('post_comment', views.post_comment)
]
