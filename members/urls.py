from django.urls import path
from . import views

urlpatterns = [
    path("login-user",views.user_login,name ="login_user"),
    path("logut-user",views.user_logout,name="logout-user"),
    path("user-register",views.user_register,name = "registration")
]
