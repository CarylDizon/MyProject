from django.contrib import admin
from .models import UserRegistration

@admin.register(UserRegistration)
class UserRegistrationAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email')  
    search_fields = ('email', 'first_name', 'last_name')  
    list_filter = ('email',) 