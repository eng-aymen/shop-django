from django.shortcuts import render,redirect
from product.models import *
# Create your views here.

def index(request):
    department = Department.objects.all()
    branch = Branch.objects.all()
    category = Category.objects.all()
    product = Product.objects.all()
    images = Image.objects.all()
    context = {
        'department':department,
        'branch':branch,
        'category':category,
        'product':product,
        'image':images,
    }
    return render(request,'pages/index.html',context)


def about(reguest):
    return render(reguest ,'pages/about.html')

def contact(request):
    return render(request ,'pages/contact.html')


def search (request):
    department = Department.objects.all()
    branch = Branch.objects.all()
    category = Category.objects.all()
    product = Product.objects.all()
    images = Image.objects.all()
    context = {
        'department':department,
        'branch':branch,
        'category':category,
        'product':product,
        'image':images,
    }
    return render(request, 'pages/search.html',context)

