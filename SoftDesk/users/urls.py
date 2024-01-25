from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView
from .views import UserViewSet

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', UserView.as_view(), name='user'),
    path('logout/', LogoutView.as_view(), name='logout')
]
