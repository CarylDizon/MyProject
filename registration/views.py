from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from .models import UserRegistration 

def authenticate_user(request):
    if request.method == "GET":
        if request.session.get("user_id"):
            return redirect('registration:user_list')
        return render(request, 'registration/login.html')

    email = request.POST.get('email', '').strip()
    password = request.POST.get('password', '')

    if not email or not password:
        messages.error(request, "Please provide both email and password.")
        return render(request, 'registration/login.html', {'email': email})

    try:
        user = UserRegistration.objects.get(email=email)
    except UserRegistration.DoesNotExist:
        messages.error(request, "Invalid credentials.")
        return render(request, 'registration/login.html', {'email': email})

    if check_password(password, user.password):
        request.session['user_id'] = user.id
        request.session['user_name'] = f"{user.first_name} {user.last_name}"
        return redirect('registration:user_list')

    if user.password == password:
        user.password = make_password(password)
        user.save(update_fields=['password'])
        request.session['user_id'] = user.id
        request.session['user_name'] = f"{user.first_name} {user.last_name}"
        return redirect('registration:user_list')

    messages.error(request, "Invalid credentials.")
    return render(request, 'registration/login.html', {'email': email})

def display_users(request):
    if not request.session.get('user_id'):
        return redirect('registration:login') 

    users = UserRegistration.objects.all().order_by('id')
    return render(request, 'registration/user_list.html', {
        'users': users,
        'current_user': request.session.get('user_name')
    }) 

def sign_out(request):
    request.session.flush()
    return redirect('home')  

def home_view(request):
    return render(request, 'registration/homepage.html')  
