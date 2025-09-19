from django.urls import path
from .views import ActivateUserView, RegisterView

urlpatterns = [
    path('auth/activate/', ActivateUserView.as_view(), name='activate_user'),
    path("register/", RegisterView.as_view(), name="register"),
]
