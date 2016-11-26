import os
import requests
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from hello.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.template import RequestContext

from .models import Greeting,List,Item

# Create your views here.

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
    'form': form
    })
 
    return render_to_response(
    'registration/register.html',
    variables,
    )
 
def register_success(request):
    return render_to_response(
    'registration/success.html',
    )
 
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')
 
@login_required
@csrf_protect
def home(request):
    if request.method == 'POST':
        form = NewListForm(request.POST)
        if form.is_valid():
            nl = List(user = request.user, title = form.cleaned_data['new_list'])
            nl.save()
            return HttpResponseRedirect('/home/')
    else:
        form = NewListForm()
    todo_listing = []  
    for todo_list in List.objects.all():
        if todo_list.user == request.user:
            todo_dict = {}
            todo_dict['list_object'] = todo_list
            todo_dict['items'] = []
            for item in Item.objects.all():
                if item.todo_list == todo_list:
                    todo_dict['items'].append(item.title)
            todo_dict['item_count'] = todo_list.item_set.count()
            todo_dict['items_complete'] = todo_list.item_set.filter(completed=True).count()
            todo_dict['percent_complete'] = int(float(todo_dict['items_complete']) / todo_dict['item_count'] * 100)  
            todo_listing.append(todo_dict)
    return render_to_response(
    'home.html',
    { 'user': request.user, 'todo_listing' : todo_listing, 'form' : form}
    )

def index(request):
    return render(request, 'index.html')

def db(request):
	greeting = Greeting()
	greeting.save()
	greetings = Greeting.objects.all()
	return render(request, 'db.html', {'greetings': greetings})

def status_report(request):
	todo_listing = []  
	for todo_list in List.objects.all():
		todo_dict = {}
		todo_dict['list_object'] = todo_list
		todo_dict['item_count'] = todo_list.item_set.count()
		todo_dict['items_complete'] = todo_list.item_set.filter(completed=True).count()
		todo_dict['percent_complete'] = int(float(todo_dict['items_complete']) / todo_dict['item_count'] * 100)  
		todo_listing.append(todo_dict)  
	return render(request,'status_report.html', {'todo_listing' : todo_listing})