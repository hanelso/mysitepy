from django.db.models import Max
from django.shortcuts import render

# Create your views here.
from user.models import User


def index(request):
    print(User.objects.aggregate(id=Max('id'))['id'])
    print(type(User.objects.aggregate(id=Max('id'))['id']))
    return render(request, 'main/index.html')
