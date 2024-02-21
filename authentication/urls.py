from django.urls import path
from . import views  # importing  views of the app-authentication

urlpatterns = [
    path('', views.index, name="index"),  # urls
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout, name="logout"),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
]
