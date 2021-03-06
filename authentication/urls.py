from django.urls import path
from authentication.views import LoginView, RegisterView, Logout, IndexView

app_name = 'authentication'
urlpatterns = [
    path('home/', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]