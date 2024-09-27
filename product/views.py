from django.shortcuts import render,get_object_or_404
from django.db.models import Q
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

def products(request):
    ##### context for navbar #####
    department = Department.objects.all()
    branch = Branch.objects.all()
    category = Category.objects.all()
    product = Product.objects.all()
    images = Image.objects.all()
    name = None
    pfrom = None
    pto = None
    ##############################
    pro = Product.objects.all()
    proo = Product.objects.all()
    dept = Department.objects.all()
    dept_search = None
    # Pagination with 3 posts per page
    paginator = Paginator(proo, 20)
    page_number = request.GET.get('page', 1)
    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
           # If page_number is not an integer deliver the first page
           products = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
           products = paginator.page(paginator.num_pages)
    type_model = 't'
    if 'searchname' in request.GET:
        name = request.GET['searchname']
        type_model = 's'
        if name:
            pro = pro.filter(p_name__icontains=name)
            print(f'{pro}########################################')

    if 'searchdesc' in request.GET:
        desc = request.GET['searchdesc']
        type_model = 's'
        if desc:
                pro = pro.filter(description__icontains=desc)

    if 'searchDept' in request.GET:
        dept_search = request.GET['searchDept']
        type_model = 's'
    category_list = []
    pro_list = []
    if 'searchpricefrom' in request.GET and 'searchpriceto' in request.GET and 'searchpricefrom' in request.GET:
        pfrom = request.GET['searchpricefrom']
        pto = request.GET['searchpriceto']
        if dept_search:
            dept = Department.objects.get(d_name=dept_search)
            br = Branch.objects.all().filter(department=dept)
            if br.exists():
                for b in br:
                    cat = Category.objects.filter(branch=b)
                    category_list.extend(cat)
                for c in category_list:
                    product_list = Product.objects.filter(category=c)
                    pro_list.extend(product_list)
        if pfrom and pto:
            if pfrom.isdigit() and pto.isdigit():
                if pro_list:
                    pro_filtered = []
                    for p in pro_list:
                        if p.price >= float(pfrom) and p.price <= float(pto):
                            pro_filtered.append(p)
                            pro = pro_filtered
                        print('$$$$$$$$$$$$$$$$$\n\n',p.price,'\n\n$$$$$$$$$$$$$$$$$$$')
                else:
                    pro = pro.filter(price__gte=pfrom , price__lte=pto)

    context = {
        ##### navbar #####
        'department':department,
        'branch':branch,
        'category':category,
        'product':product,
        'image':images,
        ##################
        'pro':pro,
        'tm':type_model,
        'name':name, 
        ###############
        'products':products,
    }
    return render(request,'product/products.html',context)
def products_dept(request,d_id):
    ##### context for navbar #####
    department = Department.objects.all()
    branch = Branch.objects.all()
    category = Category.objects.all()
    product = Product.objects.all()
    images = Image.objects.all()
    ##############################
    dept = Department.objects.get(id=d_id)
    br = Branch.objects.all().filter(department=dept)
    cat = Category.objects.all()
    pro = Product.objects.all()
    type_model = 'department'
    # Pagination with 3 posts per page
    paginator = Paginator(pro, 20)
    page_number = request.GET.get('page', 1)
    try:
        pro = paginator.page(page_number)
    except PageNotAnInteger:
           # If page_number is not an integer deliver the first page
           pro = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
           pro = paginator.page(paginator.num_pages)

    context = {
        'dept':dept,
        'br':br,
        'cat':cat,
        'pro':pro,
        'tm':type_model,
        ##### navbar #####
        'department':department,
        'branch':branch,
        'category':category,
        'product':product,
        'image':images,
        ##################
    }
    return render(request,'product/products.html',context)

def products_branch(request,b_id):
    ##### context for navbar #####
    department = Department.objects.all()
    branch = Branch.objects.all()
    category = Category.objects.all()
    product = Product.objects.all()
    images = Image.objects.all()
    ##############################
    br = Branch.objects.get(id=b_id)
    cat = Category.objects.all().filter(branch=br)
    pro = Product.objects.all()
    type_model = 'branch'

    context = {
        'br':br,
        'cat':cat,
        'pro':pro,
        'tm':type_model,
        ##### navbar #####
        'department':department,
        'branch':branch,
        'category':category,
        'product':product,
        'image':images,
        ##################
    }
    return render(request,'product/products.html',context)

def products_category(request,c_id):
    ##### context for navbar #####
    department = Department.objects.all()
    branch = Branch.objects.all()
    category = Category.objects.all()
    product = Product.objects.all()
    images = Image.objects.all()
    ##############################
    cat = Category.objects.get(id=c_id)
    pro = Product.objects.all().filter(category=cat)
    type_model = 'category'

    context = {
        'cat':cat,
        'pro':pro,
        'tm':type_model,
        ##### navbar #####
        'department':department,
        'branch':branch,
        'category':category,
        'product':product,
        'image':images,
        ##################
    }
    return render(request,'product/products.html',context)

def product(request,p_id):
    context = {
        'p':get_object_or_404(Product, pk=p_id),
    }
    return render(request,'product/detail.html',context)

def cart(request):
   
    return render(request,'product/cart.html')