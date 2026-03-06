# django-authenticate (default)
This project demonstrates a basic Django Authentication System using Django's built-in authentication framework.

## deafult user model
```
| Field        | Type          | Description           |
| ------------ | ------------- | --------------------- |
| username     | CharField     | Required, unique      |
| first_name   | CharField     | Optional              |
| last_name    | CharField     | Optional              |
| email        | EmailField    | Optional              |
| password     | CharField     | Hashed password       |
| is_staff     | BooleanField  | Admin site access     |
| is_active    | BooleanField  | Active user or not    |
| is_superuser | BooleanField  | Full permissions      |
| last_login   | DateTimeField | Last login time       |
| date_joined  | DateTimeField | Account creation time |

```
🏗 Project Structure Overview
```
django-authenticate/
│
├── core/
│   ├── settings.py        # Project settings
│   ├── urls.py            # Main URL configuration
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/              # Authentication app
│   ├── views.py           # Login, Register, Logout logic
│   ├── urls.py            # App URL routing
│   ├── models.py
│   └── migrations/
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── index.html
│   └── include/
│
├── static/                # CSS / JS files
│
├── manage.py
└── requirements.txt
```
## ⚡ 1. Setup Django (Run Project)
### Clone Repository
```
git clone https://github.com/rafi-shoishab/django-authenticate.git
cd django-authenticate
```
### Create Virtual Environment
Mac / Linux
```
python3 -m venv .venv
source .venv/bin/activate
```
Windows
```
python -m venv .venv
.venv\Scripts\activate
```
Install Dependencies
```
pip install -r requirements.txt
```
Apply Migrations
```
python manage.py migrate
```
Run Development Server
```
python manage.py runserver
```
Open Browser
```
http://127.0.0.1:8000
```
## 🔐 2. User Registration System

Users can create new accounts through the registration form.

### Registration View 
📄 accounts/views.py 
```
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

def register(request):

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Account created successfully")
        return redirect("login")

    return render(request, "register.html")
```
## 🔑 3. User Login System

Django provides built-in functions to authenticate users.

### Login View
📄 accounts/views.py

```
from django.contrib.auth import authenticate, login

def login_user(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("home")

    return render(request, "login.html") 
```
## 🚪 4. Logout System

Logout removes the user session from the server.

### Logout View
📄 accounts/views.py

```
from django.contrib.auth import logout

def log_out(request):
    logout(request)
    return redirect("login")
```

## 🔒 5. Protected Routes

Some pages should only be accessible for logged-in users.

### Django provides the login_required decorator.
📄 accounts/views.py

```
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, "index.html")
```

## 🌐 6. URL Routing

### App URLs

```
📄 accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_user, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.log_out, name="logout"),
]
```
### Project URLs
```
📄 core/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
]
```
## 🎨 7. Template System

Templates are used to render HTML pages.

📄 templates/login.html

```
<form method="POST">
    {% csrf_token %}

    <input type="text" name="username" placeholder="Username">

    <input type="password" name="password" placeholder="Password">

    <button type="submit">
        Login
    </button>
</form>
```

## 🔁 Django Authentication Flow
```
User Request
     ↓
urls.py
     ↓
views.py
     ↓
authenticate()
     ↓
login()
     ↓
Session Created
     ↓
User Logged In
```

## 🛠 Django Admin Panel
### Apply Migrations
```
python manage.py migrate
```
### Create Superuser
```
python manage.py createsuperuser
```
### Login Admin Panel
```
http://127.0.0.1:8000/admin/
```
## 🔧 Git Workflow (Quick Guide)

### First Time
```
git add .

git commit -m "initial commit"

git push -u origin main
```

### Daily Workflow

```
git pull

git add .

git commit -m "update message"

git push
```
## 📄 Recommended .gitignore
```
.venv/

venv/

__pycache__/

*.pyc

db.sqlite3

.DS_Store
.vscode/
media/
```
## 👨‍💻 Author
Rafiur Rahman Shoishab

GitHub:
https://github.com/rafi-shoishab

## 📜 License
This project is created for educational purposes to learn Django authentication.
