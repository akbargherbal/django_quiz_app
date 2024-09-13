# Django Authentication Reference Guide
[User registration and authentication in Django](https://youtu.be/Z3qTXmT0yoI)

## Table of Contents
1. [Project Setup](#project-setup)
2. [User Registration](#user-registration)
3. [User Login](#user-login)
4. [User Logout](#user-logout)
5. [Protecting Views](#protecting-views)
6. [Additional Notes](#additional-notes)

## Project Setup

### Create a Django Project (Minute 0-2)
1. Create a folder for your Django projects
2. Open command prompt and navigate to the folder
3. Install virtual environment: `pip install virtualenv`
4. Create a virtual environment: `virtualenv venv`
5. Activate the virtual environment: `venv\scripts\activate`
6. Install Django: `pip install django`
7. Create a Django project: `django-admin startproject projectname`
8. Navigate to the project folder: `cd projectname`
9. Create a Django app: `python manage.py startapp appname`

### Configure Settings (Minute 4-5)
1. In `settings.py`, add your app to `INSTALLED_APPS`:
   ```python
   INSTALLED_APPS = [
       ...
       'appname',
   ]
   ```

## User Registration

### Create User Registration Form (Minute 25-28)
1. In your app folder, create `forms.py`
2. Import necessary modules:
   ```python
   from django.contrib.auth.forms import UserCreationForm
   from django.contrib.auth.models import User
   from django import forms
   ```
3. Create a custom user creation form:
   ```python
   class CreateUserForm(UserCreationForm):
       class Meta:
           model = User
           fields = ['username', 'email', 'password1', 'password2']
   ```

### Set Up Registration View (Minute 29-31)
1. In `views.py`, import the form and necessary functions:
   ```python
   from .forms import CreateUserForm
   from django.shortcuts import render, redirect
   ```
2. Create the registration view:
   ```python
   def register(request):
       form = CreateUserForm()
       if request.method == "POST":
           form = CreateUserForm(request.POST)
           if form.is_valid():
               form.save()
               return redirect("my-login")
       context = {'registerform': form}
       return render(request, 'appname/register.html', context=context)
   ```

### Create Registration Template (Minute 20-21)
1. In your app's `templates` folder, create `register.html`:
   ```html
   <h1>Register now!</h1>
   <form method="POST" autocomplete="off">
       {% csrf_token %}
       {{registerform.as_p}}
       <input type="submit" value="Register"/>
   </form>
   ```

## User Login

### Create Login Form (Minute 40-42)
1. In `forms.py`, add:
   ```python
   from django.contrib.auth.forms import AuthenticationForm
   from django.forms.widgets import PasswordInput, TextInput

   class LoginForm(AuthenticationForm):
       username = forms.CharField(widget=TextInput())
       password = forms.CharField(widget=PasswordInput())
   ```

### Set Up Login View (Minute 44-47)
1. In `views.py`, import necessary functions:
   ```python
   from django.contrib.auth import authenticate, login
   from .forms import LoginForm
   ```
2. Create the login view:
   ```python
   def my_login(request):
       form = LoginForm()
       if request.method == 'POST':
           form = LoginForm(request, data=request.POST)
           if form.is_valid():
               username = request.POST.get('username')
               password = request.POST.get('password')
               user = authenticate(request, username=username, password=password)
               if user is not None:
                   login(request, user)
                   return redirect("dashboard")
       context = {'loginform': form}
       return render(request, 'appname/my-login.html', context=context)
   ```

### Create Login Template (Minute 21-22)
1. Create `my-login.html`:
   ```html
   <h1>Login here</h1>
   <form method="POST" autocomplete="off">
       {% csrf_token %}
       {{loginform.as_p}}
       <input type="submit" value="Login"/>
   </form>
   ```

## User Logout

### Set Up Logout View (Minute 50-51)
1. In `views.py`, add:
   ```python
   from django.contrib.auth import logout

   def user_logout(request):
       logout(request)
       return redirect("")
   ```

### Add Logout Link (Minute 52-53)
1. In your dashboard template, add:
   ```html
   <a href="{% url 'user-logout' %}">Logout here</a>
   ```

## Protecting Views

### Use Login Required Decorator (Minute 54-55)
1. In `views.py`, import the decorator:
   ```python
   from django.contrib.auth.decorators import login_required
   ```
2. Apply the decorator to views that require authentication:
   ```python
   @login_required(login_url="my-login")
   def dashboard(request):
       return render(request, 'appname/dashboard.html')
   ```

## Additional Notes

- Create a superuser for admin access: `python manage.py createsuperuser` (Minute 37-38)
- Always use `csrf_token` in forms for security
- Customize the User model fields as needed in your `CreateUserForm`
- Use `auth.login()` instead of just `login()` to avoid naming conflicts
- Remember to set up proper URL patterns in `urls.py` for all views
- Test the authentication flow thoroughly to ensure it works as expected

