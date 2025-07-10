from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register, name='register'),
    path('login/',views.login, name='login'),
    path('users_data/',views.users_data, name='users_data'),
    path('logout/', views.logout, name='logout'),
]
