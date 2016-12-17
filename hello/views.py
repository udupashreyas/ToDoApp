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
        if 'new_list' in request.POST:
            l_form = NewListForm(request.POST)
            if l_form.is_valid():
                nl = List(title = l_form.cleaned_data['list_title'])
                nl.save()
                nl.users.add(request.user)
        elif 'new_item' in request.POST:
            i_form = NewItemForm(request.POST)
            if i_form.is_valid():
                ni = Item(title = i_form.cleaned_data['title'], priority = i_form.cleaned_data['priority'], todo_list = i_form.cleaned_data['p_list'])
                ni.save()
        elif 'done' in request.POST:
            i = request.POST['done']
            it = Item.objects.get(title=i)
            it.completed = True
            it.save()
        elif 'undone' in request.POST:
            i = request.POST['undone']
            it = Item.objects.get(title=i)
            it.completed = False
            it.save()
        elif 'remove' in request.POST:
            i = request.POST['remove']
            it = Item.objects.get(title=i)
            it.delete()
        elif 'del_list' in request.POST:
            i = request.POST['del_list']
            it = List.objects.get(title=i)
            it.delete()
        elif 'share_list' in request.POST:
            s_form = ShareListForm(request.POST)
            if s_form.is_valid():
                sl = List.objects.get(title=s_form.cleaned_data['p_list'].title)
                sl.users.add(User.objects.get(username=s_form.cleaned_data['other_user']))
    l_form = NewListForm()
    i_form = NewItemForm()
    s_form = ShareListForm()
    i_form.fields['p_list'].queryset = List.objects.filter(users__in=[request.user])
    s_form.fields['p_list'].queryset = List.objects.filter(users__in=[request.user])
    todo_listing = []  
    for todo_list in List.objects.all():
        if request.user in todo_list.users.all():
            todo_dict = {}
            todo_dict['list_object'] = todo_list
            todo_dict['list_title'] = todo_list.title
            todo_dict['it'] = {}
            for item in Item.objects.all():
                if item.todo_list == todo_list:
                    todo_dict['it'][item.title] = item.completed
            todo_dict['item_count'] = todo_list.item_set.count()
            todo_dict['items_complete'] = todo_list.item_set.filter(completed=True).count()
            if todo_dict['item_count']:
                todo_dict['percent_complete'] = int(float(todo_dict['items_complete']) / todo_dict['item_count'] * 100)
            else:
                todo_dict['percent_complete'] = 0
            todo_listing.append(todo_dict)
    return render_to_response(
    'home.html',
    { 'user': request.user, 'todo_listing' : todo_listing, 'l_form' : l_form, 'i_form' : i_form, 's_form' : s_form},
    RequestContext(request)
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