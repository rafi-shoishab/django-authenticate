from django.shortcuts import render, redirect 
from django.contrib.auth.models import User # default model import
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash #login 
from django.contrib.auth.decorators import login_required 
from django.contrib import messages # show msg 
import re # for password pattern regex 


# Create your views here.
def home(request):
    return render(request, 'accounts/index.html')

def register(request):

    if request.method == "POST":
        user_name = request.POST.get('user_name')  # variable = ....('html name')
        firstname = request.POST.get('first_name') 
        lastname = request.POST.get('last_name') 
        mail = request.POST.get('email') 
        password = request.POST.get('password') 
        confirm_password = request.POST.get('confirm_password') 

        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

        if password != confirm_password:
            messages.error(request, "wrong password")
            return redirect('register') # urls name
        
        if not re.match(pattern, password):
            messages.error(request, "password at leat 8 characters: includes [0-9][a-z][A-Z][!@#$%^&?...]")
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


    return render(request, 'accounts/register.html') # template url name

def log_in(request): 

    if request.method == "POST": 
        username_email = request.POST.get('username_or_email')
        pass_word = request.POST.get('password')

        # if username or email : error handle with try & except
        try:
            user_obj = User.objects.get(email = username_email) # object = ....(modelname = variable)
            user_name = user_obj.username  # variable = object.modelname
        except User.DoesNotExist: 
            user_name = username_email 
        
        user = authenticate(request, username = user_name, password = pass_word)  # variable = ...(modelname = variable)
        
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

@login_required
def log_out(request):

    logout(request)
    messages.success(request, 'Logged out Successfully')

    return redirect('login')

def profile(request):

    return render(request, 'accounts/profile.html')

@login_required
def edit_profile(request):

    pro_file = request.user  # get the default model in a variable        

    if request.method == "POST":

        pro_file.first_name = request.POST.get('first_name') # variable.default_model_name = ...('html name')
        pro_file.last_name = request.POST.get('last_name')
        pro_file.email = request.POST.get('email')
        password = request.POST.get('password') # default_model_name = ...(html name)
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "password unmatched")
            return redirect('edit_profile')
        
        if not pro_file.check_password(password):
            messages.error(request, "password unmatched")
            return redirect('edit_profile')

        pro_file.save()
        messages.success(request, "profile updated successfully") 
        return redirect('profile') 
    
    context = {
        'data' : pro_file
    }
    return render(request, 'accounts/edit_profile.html', context)

@login_required
def change_password(request):

    pro_file = request.user  # get the default model in a variable
    if request.method == "POST":

        old_password = request.POST.get('old_password') # default_model_name = ...(html name)
        new_password = request.POST.get('new_password') 
        confirm_password = request.POST.get('confirm_new_password')

        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

        if new_password != confirm_password:
            messages.error(request, 'password did not match')
            return redirect('change_password')
    
        if not re.match(pattern, new_password):
            messages.error(request, "password at leat 8 characters: includes [0-9][a-z][A-Z][!@#$%^&?...]")
            return redirect ('change_password')

        if not pro_file.check_password(old_password):
            messages.error(request, "wrong old password!")
            return redirect('change_password') 
        
        pro_file.set_password(new_password) 
        update_session_auth_hash(request, pro_file) # update password of the user
        pro_file.save()
        messages.success(request, 'password changed successfully')
        return redirect('profile')

    return render(request, 'accounts/change_password.html')