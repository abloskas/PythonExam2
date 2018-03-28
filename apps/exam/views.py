from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
import bcrypt
from .models import *
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your views here.

def index(request):
    return render(request, 'exam/index.html')

def dashboard(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['id'])
        }
        return render(request, 'exam/dashboard.html', context)     

def loading(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    first_name = request.POST['fname'] 
    last_name = request.POST['lname']
    email = request.POST['email']
    password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=password)
    request.session['id'] = user.id
    return redirect('/dashboard')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    email = request.POST['email']
    request.session['id'] = User.objects.get(email=email).id
    return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect('/')   