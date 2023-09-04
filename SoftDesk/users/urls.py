from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView
from .views import UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')
urlpatterns = router.urls
urlpatterns += [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/', UserView.as_view(), name='user'),
    path('logout/', LogoutView.as_view(), name='logout')
]
