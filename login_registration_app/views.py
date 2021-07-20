from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
import bcrypt

def index(request):
    # if 'user' in request.session:
    #     del request.session['user']
    return render(request, 'index.html')


def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)

        request.session['reg_first_name'] = request.POST['first_name']
        request.session['reg_last_name'] = request.POST['last_name']
        request.session['reg_birthday'] = request.POST['birthday']
        request.session['reg_email'] = request.POST['email']

        return redirect('/') 

    else:
        if 'reg_first_name' in request.session:
            del request.session['reg_first_name']
        if 'reg_last_name' in request.session:
            del request.session['reg_last_name']
        if 'reg_birthday' in request.session:
            del request.session['reg_birthday']
        if 'reg_email' in request.session:
            del request.session['reg_email']
        
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            birthday = request.POST['birthday'],
            email = request.POST['email'],
            password = pw_hash
        )

        messages.success(request, 'User succesfully created') 

        return redirect('/')


def login(request):
    errors = User.objects.login_validator(request.POST)
    # print(request.POST['email'])
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')

    else:
        if 'user' in request.session:
            messages.error(request, "You're already logged")
            return redirect('/success')
        user = User.objects.filter(email=request.POST['email'])
        logged_user = user[0]
        userlogged = {
            'id': logged_user.id,
            'first_name': logged_user.first_name,
            'last_name': logged_user.last_name,
            'email': logged_user.email
            }
        request.session['user'] = userlogged
        messages.success(request, 'User succesfully logged')
        return redirect('/success')


def success(request):
    if 'user' not in request.session:
        return redirect('/')
    return render(request, 'success.html')


def logout(request):
    request.session.flush()
    return redirect('/')

