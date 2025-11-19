from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include

app_name = "registration"

urlpatterns = [
    path('api/create/', views.create_user, name='create_user'),
    path('api/all-users/', views.get_all_users, name='get_all_users'),
    path('api/user/<int:pk>/', views.manage_user, name='manage_user'),
    
    path('signin/', views.authenticate_user, name='login_html'),
    path('signout/', views.sign_out, name='logout_html'),
    path('user-list/', views.display_users, name='users_html'),
    path('admin/', admin.site.urls),
    path('home', views.home_view, name='homepage_html'),

]