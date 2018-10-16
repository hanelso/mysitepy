from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from guestbook import models
from guestbook.models import Guestbook


def index(request):
    # results = models.fetchall()
    results = Guestbook.objects.all().order_by('-id')
    data = {"guestbook_list":results}
    return render(request, 'guestbook/index.html', data)


def deleteform(request):
    id = request.GET['id']
    data = {"id":id}
    return render(request, 'guestbook/deleteform.html', data)


def add(request):
    guestbook = Guestbook()

    guestbook.name = request.POST['name']
    guestbook.password = request.POST['password']
    guestbook.message = request.POST['message']

    guestbook.save()

    return HttpResponseRedirect("/guestbook")


def delete(request):

    id = request.POST['id']
    password = request.POST['password']
    data = {"id":id, "password":password}

    Guestbook.objects.filter(id=id).filter(password=password).delete()

    return HttpResponseRedirect("/guestbook", data)