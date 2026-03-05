from django.shortcuts import render, redirect 
from django.contrib.auth.models import User # default model import
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash #login 
from django.contrib import messages # show msg 

# Create your views here.
def home(request):
    return render(request, 'accounts/index.html')

def register(request):

    if request.method == 'POST':
        user_name = request.POST.get('user_name') 
        firstname = request.POST.get('first_name') 
        lastname = request.POST.get('last_name') 
        mail = request.POST.get('email') 
        password = request.POST.get('password') 
        confirm_password = request.POST.get('confirm_password') 

        if password != confirm_password:
            messages.error(request, 'wrong password')
            return redirect('register')
        
        if User.objects.filter(username = user_name).exists():
            messages.error(request, 'username already exists')
            return redirect('register')
        
        if User.objects.filter(email = mail).exists():
            messages.error(request, 'mail already exists')
            return redirect('register')
        
        # Create user with hased password for using create_user()
        user = User.objects.create_user(
            username = user_name,  # modelname = variable
            email = mail,
            password = password 
        ) 

        user.first_name = firstname  # user.modelname = variable  
        user.last_name = lastname 

        user.save()
        messages.success(request, 'account created succesfully')
        return redirect('login')


    return render(request, 'accounts/register.html')

def signin(request):

    if request.method == "POST":
        username_email = request.POST.get('username_or_email')
        pass_word = request.POST.get('password')

        # if username or email : error handle with try & except
        try:
            user_obj = User.objects.get(email = username_email) # object = ....(modelname = variable)
            user_name = user_obj.username  # variable = object.modelname
        except User.DoesNotExist:
            user_name = username_email  
        
        user = authenticate(request, username = user_name, password = pass_word)  # variable = ...(modelname = vriable)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login Successfull')
            return redirect('home')
        
        else:
            messages.error(request, 'Invalid Credential!')
            return redirect('login')
        

        # if only username
        '''user = authenticate(request, username = username_email, password = pass_word)
        if user is not None:
            login(request, user)
            messages.success(request,'login successfull')
            return redirect('home')
        else:
            messages.error(request, 'invalid input')
            return redirect('login')'''

    return render(request, 'accounts/login.html')

def profile(request):

    return render(request, 'accounts/profile.html')