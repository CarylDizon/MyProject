from django.urls import path
from . import views

app_name = "registration"

urlpatterns = [
    path('login/', views.authenticate_user, name='login'),  
    path('users/', views.display_users, name='user_list'),  
    path('logout/', views.sign_out, name='logout'),
]