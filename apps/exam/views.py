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
            'user': User.objects.get(id=request.session['id']),
            'favorites': Quotes.objects.filter(others=request.session['id']),
            'quotes': Quotes.objects.filter(~Q(others=request.session['id']))
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

# create a new item from dashboard page, GET
def create(request):   
    if request.POST['name']:
        item = Quotes.objects.create(name=request.POST['name'], quote=request.POST['quote'], user=User.objects.get(id=request.session['id']))
        this_item = Quotes.objects.get(name=request.POST['name'], quote=request.POST['quote'])
        this_user = User.objects.get(id=request.session['id'])
        this_item.others.add(this_user)
    else:
        messages.error(request, 'Please enter a Quote Author and Quote!') 
        return redirect('/users/dashboard')   
    return redirect('/users/dashboard') 
    

def quote(request, id):
    context = {
        'username': User.objects.get(id=id),
        'quotes': Quotes.objects.filter(user_id=id)
    }
    return render(request, 'exam/quote.html', context)      

def delete(request, id):
    item = Quotes.objects.get(id=id)   
    item.delete()
    return redirect('/users/dashboard')

def remove(request ,id):
    if 'id' in request.session:
        this_item = Quotes.objects.get(id=id)
        this_user = User.objects.get(id=request.session['id'])
        this_item.others.remove(this_user)
        return redirect('/users/dashboard')  


def add(request, id): 
    if 'id' in request.session:
        this_item = Quotes.objects.get(id=id)
        this_user = User.objects.get(id=request.session['id'])
        this_item.others.add(this_user)
        return redirect('/users/dashboard')      