from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm

def signup(request):
    user = request.user
    if user.is_authenticated:
        messages.add_message(request, messages.INFO, 'Please logout first to signup')
        return redirect('home')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            new_user.set_password(password)
            new_user.save()
            messages.add_message(request, messages.SUCCESS, 'User Registered Succesfully')
            return redirect('login')
        else:
            messages.add_message(request, messages.ERROR, 'Please Enter Data Correctly')
            return render(request, 'signup.html', {'form': form})
    else:
        return render(request, 'signup.html', {'form': SignupForm()})

def check_signup(request):
    if request.method == 'POST':
        field = request.POST.get('form')
        field_type = request.POST.get('form_type')
        print (field_type)
        status = True
        msg = 'This '+ field_type +' is available'
        context = {}
        if field_type == 'email':
            try:
                if User.objects.filter(email__iexact=field):
                    status = False
                    msg = 'This email is not available'
            except:
                pass
        elif field_type == 'username':
            try:
                if User.objects.filter(username__iexact=field):
                    status = False
                    msg = 'This username is not available'
            except:
                pass
        else:
            status = False
            msg = 'Something Wrong happened please try again'

        context = {
            'status': status,
            'msg': msg
        }
        return JsonResponse(context)

def signin(request):
    user = request.user
    if user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
         
            password = form.cleaned_data.get('password')
        
        else:
            messages.add_message(request, messages.ERROR, 'Form Not Valid')
            return (redirect('login'))
        if '@' in username:
            try:
                user = authenticate(email=username, password=password)
            except:
                messages.add_message(request, messages.ERROR, 'Something Wrong Happened, Please try again')
                return redirect('login')
        else:
            try:
                user = authenticate(username=username, password=password)
            except:
                messages.add_message(request, messages.ERROR, 'Something Wrong Happened, Please try again')
                return redirect('login')
        try:
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.add_message(request, messages.ERROR, 'User you are trying to logging is not active')
                    return redirect('login')
            else:
                messages.add_message(request, messages.ERROR, 'User Doesn\'t exist')
                return redirect('login')
        except:
            messages.add_message(request, messages.ERROR, 'Something Wrong Happened, Please try again')
            return redirect('login')
    else:
        return render(request, 'login.html', {'form': LoginForm()})

def signout(request):
    user = request.user
    if user.is_authenticated:
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'You have logged out')
        return redirect('signin')
    else:
        messages.add_message(request, messages.SUCCESS, 'You are already logged out')
        return redirect('signin')