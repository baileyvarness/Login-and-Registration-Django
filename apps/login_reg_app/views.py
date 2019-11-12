from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, "index.html")


def register(request):
    print('request.POST: ', request.POST)
    errors = Users.objects.validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        # hash password
        hashed_password = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt())
        new_user = Users.objects.create(first_name=request.POST['first_name'],
                                       last_name=request.POST['last_name'],
                                       email=request.POST['email'],
                                       password=hashed_password)
        if new_user:
            request.session['uid'] = new_user.id
        else:
            print('there was a problem creating the user')
            return redirect('/')

    return redirect('/success')



def login(request):
    user_list = Users.objects.filter(email=request.POST['email'])
    if len(user_list) > 0:
        hashed_password = user_list[0].password
        if bcrypt.checkpw(request.POST['password'].encode(), hashed_password.encode()):
            request.session['uid'] = user_list[0].id
            return redirect('/success')
        else:
            messages.error(request, 'invalid email and/or password')
    else:
        messages.error(request, 'invalid email and/or password')
    return redirect('/')

def success(request):
    if 'uid' not in request.session:
        print('we do not have a user id in session')
        return redirect('/')
    context = {
        'user': Users.objects.get(id=request.session['uid'])
    }
    return render(request, 'success.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')