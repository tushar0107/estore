from django.shortcuts import render

# Create your views here.
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


class ProductListView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get(self):
        search_product = self.request.query_params.get('search')
        order = self.request.query_params.get('order')
        category = self.request.query_params.get('categories')
        queryset1 = Product.objects.filter(name__icontains=search_product)
        queryset2 = Product.objects.filter(desc__icontains=search_product)
        #searches for products only if order and category parameter is passed
        if order is not None:
            #if "order" parameter has some value ('price' or 'desc') this searches within category
            #and returns the union of both query sets
            if category is not None:
                queryset3 = Product.objects.filter(category=category)
                return queryset1.union(queryset2).union(queryset3).order_by(order)
            return queryset1.union(queryset2).order_by(order)
        
        #if 'order' parameter is not passed but 'category is passed
        elif category is not None:
            queryset3 = Product.objects.filter(category=category)
            return queryset1.union(queryset3).order_by("price")
        
        #to search products with only categories or if 'search parameter is not passed
        elif search_product is None:
            return queryset3
        
        #if 'category' parameter is not passed
        else:
            return queryset1.union(queryset2)

#class based view to get product by "id"
class ProductView(generics.CreateAPIView):
    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

def get_csrf_token(request):
    csrf_token = csrf.get_token(request)
    return JsonResponse({'csrfToken': csrf_token})


@method_decorator(csrf_protect, name='dispatch')
class LoginView(APIView):
    
    # user login view
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        print(user)
        # if user has logged in with valid credentials
        if user is not None:
            login(request, user)
            user = User.objects.get(username=username)
            userdata = {'id': user.id,'username': user.username,'first_name': user.first_name, 'last_name':user.last_name,'email':user.email}
            return Response({
                'message': 'Logged In Successfully',
                'data': userdata,
                })
        else:
            return Response({
                'message': 'Invalid credentials',
                })
        
    def get(self, request, id=None):
        if request.user.is_authenticated and request.user.id==id:
            if Customer.objects.filter(user=request.user).exists():
                customer = Customer.objects.get(user=request.user)
                customer = CustomerSerializer(customer, many=False)
                return Response({
                    'data': customer.data,
                })
            else:
                return Response({
                    'message': 'User details not provided',
                    'status': False,
                })
        else:
            return Response({
                'message': 'Please Login.'
            })

@method_decorator(csrf_protect, name='dispatch')
class RegisterUser(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        
        # user = authenticate(request, username=username, password=password)
        if User.objects.filter(username=username).exists():
            return Response({
                'message': 'Mobile number exists.\n Please Try with a different Mobile number.'
            })
        else:
            user = User.objects.create_user(
                username = username,
                password = password,
                first_name = first_name,
                last_name = last_name
            )
            user.save()
            login(request, user)
            
            userdata = {'username': user.username,'first_name': user.first_name, 'last_name':user.last_name,'email':user.email}
            return Response({
                'message': 'User Registered Successfully',
                'data':{
                    'user': str(userdata),
                }
            })

class CustomerCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        phone = request.data.get('mobile')
        plot_no = request.data.get('plot_no')
        streetaddr = request.data.get('address')
        pincode = request.data.get('pincode')
        city = request.data.get('city')

        user = authenticate(request, username=username, password=password)
        if request.user.is_authenticated:
            if Customer.objects.filter(user=request.user).exists():
                return Response({
                    'message': 'You have already registered as a customer. Please login.'
                })

            elif User.objects.filter(email=email).exists():
                return Response({
                    'message': 'This emailId is already registered.'
                })
            else:
                user = User.objects.get(username=username)
                user.email = email
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                customer = Customer.objects.create(
                    user= user,
                    phone = username,
                    plot_no = plot_no,
                    streetaddr = streetaddr,
                    city = city,
                    pincode = pincode,
                )
                customer.save()
                userdata = {'username': user.username,'first_name': user.first_name, 'last_name':user.last_name,'email':user.email}
                customer = CustomerSerializer(customer, many=False)
                return Response({
                    'message': 'User Registered',
                    'data': {
                        'user': str(userdata),
                        'customer': str(customer.data)
                    }
                })
        else:
            return Response({
                'message': 'Please Login',
            })

