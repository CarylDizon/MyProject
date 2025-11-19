from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.urls import reverse

# Import your models and serializers
from registration.models import UserRegistration
from registration.serializer import RegistrationSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def create_user(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_users(request):
    users = UserRegistration.objects.all()
    serializer = RegistrationSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Handle user details for GET, PUT, DELETE
@api_view(['GET', 'PUT', 'DELETE'])
def manage_user(request, pk):
    try:
        user = UserRegistration.objects.get(pk=pk)
    except UserRegistration.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RegistrationSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = RegistrationSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            # Log errors for debugging
            print("Validation errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Authentication view for login
def authenticate_user(request):
    if request.method == "GET":
        if request.session.get("user_id"):
            return redirect('registration:users_html')
        return render(request, 'registration/login.html')

    email_input = request.POST.get('email', '').strip()
    password_input = request.POST.get('password', '')

    if not email_input or not password_input:
        messages.error(request, "Please provide both email and password.")
        return render(request, 'registration/login.html', {'email': email_input})

    try:
        user = UserRegistration.objects.get(email=email_input)
    except UserRegistration.DoesNotExist:
        messages.error(request, "Invalid login details.")
        return render(request, 'registration/login.html', {'email': email_input})

    if check_password(password_input, user.password):
        request.session['user_id'] = user.id
        request.session['user_name'] = f"{user.first_name} {user.last_name}"
        return redirect('registration:users_html')

    # Handle legacy unhashed passwords by hashing them on first login
    if user.password == password_input:
        user.password = make_password(password_input)
        user.save(update_fields=['password'])
        request.session['user_id'] = user.id
        request.session['user_name'] = f"{user.first_name} {user.last_name}"
        return redirect('registration:users_html')

    messages.error(request, "Invalid login details.")
    return render(request, 'registration/login.html', {'email': email_input})

# Logout functionality
def sign_out(request):
    request.session.flush()
    return redirect('home_html')

# Decorator to enforce login requirement
def require_login(fn):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect(f"{reverse('registration:login_html')}?next={request.path}")
        return fn(request, *args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper

# View for displaying users list (requires login)
@require_login
def display_users(request):
    users = UserRegistration.objects.all().order_by('id')
    return render(request, 'registration/users_list.html', {
        'users': users,
        'current_user': request.session.get('user_name')
    }) 

def sign_out(request):
    request.session.flush()
    return redirect('home')  

def home_view(request):
    return render(request, 'registration/homepage.html')  