from django.shortcuts import render, redirect

from .models import *
from django.db.models import Count
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from django.http import JsonResponse
from django.middleware import csrf

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets,status, generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from estore.serializer import *

import json


# Create your views here.

def index(request):
	return render(request,'home.html',context={'name':'Tushar','items':enumerate([1,2,3,4,5,6,7,8,9])})

def product_list(request):
    query = request.GET.get('product', '')
    category = request.GET.get('categories', '')
    
    products = Product.objects.all()
    
    if query:
        products = products.filter(name__icontains=query)
    if category:
        products = products.filter(category__name__icontains=category)
        
    return render(request, 'product_list.html', {'products': products})

def product_detail(request, slug):
    try:
        product = Product.objects.get(slug_field=slug)
        return render(request, 'product.html', {'product': product})
    except Product.DoesNotExist:
        return render(request, '404page.html')


def profile(request):
    #to go to profile page of the user
    print(request.user.id)
    if(request.user.id is not None):
        customer = Customer.objects.get(user=request.user) if Customer.objects.filter(user=request.user).exists() else None
        orders = Order.objects.filter(user=request.user)
        return render(request, 'profile.html', {'logo': "Profile",'customer':customer,'orders':orders})
    else:
        return render(request, 'profile.html')
    
#user login form
def user_login(request):
    #gets form input only if the form action method is POST
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        #this function works only if user is not logged in 
        if user is not None:
            login(request,user)
            return redirect(profile)
        else:
            messages.warning(request,'Invalid Credentials. Try again.')
        return redirect(profile)
    else:
        return redirect(profile)
    

#user registration form
def signup(request):
    #gets form input only if the form action method is POST
    if request.method == 'POST':
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')

        #checks if email is already registered or not,
        #if already registred email found, it sends a message and redirects to login
        if User.objects.filter(email=email).exists():
            messages.warning(request,'Email already registered. Login or try another email.')
            return redirect(profile)
        
        #checks if username is already registered or not,
        #if already registred username found, it sends a message and redirects to login
        if User.objects.filter(username=username).exists():
            messages.warning(request, 'Username has been used already, Try Logging in.')
            return redirect(profile)
        #if all credentials are valid a user object is created
        else:
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=firstname,
                last_name=lastname
            )
            user.save()
            # user = auth.authenticate(request,username=username,password=password)    #to save the new user object
            login(request,user)  #to log in the new user
            return redirect(index)

def products(request):
    #fetch out the products from the database with the filter
    search_product = request.GET.get('product')
    category = request.GET.get('categories')
    order = request.GET.get('order')

    products_list = Product.objects.none()
    if search_product is not None:
        products_list = Product.objects.filter(name__icontains=search_product)
    if category is not None:
        categories = Category.objects.filter(slug=category).only('id')
        print(categories)
        products_by_category = Product.objects.filter(category__in=categories)

        if order is not None:
            products_list = list(products_list.union(products_by_category).order_by(order))
        else:
            products_list = list(products_list.union(products_by_category))
    
    if len(products_list)!=0:
        #counts the number of products found in the database
        num_of_products = len(products_list)
        if search_product is not None:
            search_param = search_product 
        elif category is not None:
            search_param = category
        return render(request,'products.html',{
            'products':products_list,
            'num_of_products':num_of_products,
            'search':search_param,
            'logo':"STORE"})

    else:
        #returns nothing if no products found with the relevant name
        num_of_products = '0'
        if search_product is not None:
            search_param = search_product 
        elif category is not None:
            search_param = category
        return render(request, 'products.html',{'logo':"STORE",'num_of_products':num_of_products,'search':search_param,})

def product(request, slug):
    if Product.objects.filter(slug_field=slug).exists():
        product = Product.objects.get(slug_field=slug)
        return render(request, 'product.html',{'logo':'STORE','product':product})
    else:
        return render(request, '404page.html')


def products_by_category(request):
    #fetch products from the database by filtering through categories
    pass

def update_cart(request):
    if request.method == 'POST':
        if(request.POST.get('method')=='delete'):
            product_id = request.POST.get('product_id')
            print(product_id)
            product=Product.objects.get(id=product_id)
            Cart.objects.filter(product=product).delete()
            return JsonResponse({'message':'Product removed from cart'})
        else:
            product_id = request.POST.get('product_id')
            product = Product.objects.get(id=product_id)
            Cart.objects.create(user=request.user, product=product)
            return JsonResponse({'message':'Product has been added to Cart successfully'})
      
    else:
        return JsonResponse({'error':'Invalid request Method'})


@login_required(login_url='/login/')
def cart(request):
    cartQuery = Cart.objects.filter(user=request.user)# gets cart objects for current user
    cartList = [item.product for item in cartQuery] #converts the queryset into list
    cartDict = {}       #dictionary usage is correct here
    # modify cartDict to add quantity of products and total price to the cart
    for i in cartList:
        if i not in cartDict:
            cartDict[i] = cartList.count(i)
            i.quantity = cartDict[i]
            i.tot_price = i.price * i.quantity
    return render(request, 'cart.html', {'logo':'Cart','cartDict':cartDict,'len_of_cart':len(cartDict)})


def create_order_item(request):
    cart = request.POST.get('cart')
    cartArr = json.loads(cart)
    print(cartArr)
        
    return JsonResponse({'message':'Order created successfully'})

#for checkout the user must have to go through the cart and modify items and then confirm checkout
@login_required(login_url='/login/')
def checkout(request,id=None):
    user = User.objects.get(id=request.user.id)
    if(Customer.objects.filter(user=user).exists()):
        print(user)
        customer = Customer.objects.get(user=user)
        total_price = 0
        order_items = OrderItem.objects.filter(user=user)

        for order in order_items:
            total_price = total_price + order.total_amount
        messages.success(request,'Order recorded successfully. Please confirm the order and other details')
        return render(request, 'checkout.html', {'logo':'Checkout','customer':customer, 'total_amount':total_price})
    else:
        return JsonResponse({'message': 'Need More customer details. Please fill out your details from the profile'},status=404)


def confirm_order(request):
    user = User.objects.get(id=request.user.id)
    orders = OrderItem.objects.filter(user=user,status=False)
    total_price = request.POST.get('total_price')
    plot_no = request.POST.get('plot-no')
    strt_addr = request.POST.get('strt-address')
    payment_mode = request.POST.get('payment_mode')
    print(user, orders,total_price, plot_no, strt_addr, payment_mode)
    print([order.id for order in orders])
    ord = Order.objects.create(
        user=user,
        delivery_address=plot_no+', '+strt_addr,
        total_price=total_price,
        payment_mode=payment_mode
    )
    ord.save()
    for order in orders:
        ord.order.add(order.id)
    return redirect(profile)

def user_logout(request):
    #to logout the user
    if request.user.is_authenticated:
        logout(request)
        messages.info(request,"Logged Out.")
        return redirect(index)

def delete_account(request):
    #to delete the user account
    try:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if(user is not None):
            user.delete()
        messages.success(request,"User deleted. Redirecting you to home.")
        return redirect(index)
    except User.DoesNotExist:
        messages.error(request,"User does not exists.")
        return redirect(index)
