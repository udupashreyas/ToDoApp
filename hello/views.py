import os
import requests
from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting,List

# Create your views here.
def index(request):
    times = int(os.environ.get('TIMES',3))
    return HttpResponse('Hello! ' * times)

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