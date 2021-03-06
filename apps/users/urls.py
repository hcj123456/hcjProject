from django.urls import path, re_path
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token
from users import views

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('register/', views.UserView.as_view({
        'post': 'create',
    })),
]