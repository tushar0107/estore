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
from store.serializer import *

import json


# Create your views here.

def index(request):
	return render(request,'home.html',context={'name':'Tushar','items':enumerate([1,2,3,4,5,6,7,8,9])})

def page(request):
	return render(request,'page.html',context={'page':'second page'})

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
        return render(request, 'product_detail.html', {'product': product})
    except Product.DoesNotExist:
        return render(request, '404page.html')