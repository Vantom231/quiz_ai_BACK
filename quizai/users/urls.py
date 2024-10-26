from django.urls import path
from .views import RegisterView, LoginView, UserView, LogOutView

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogOutView.as_view())
]
