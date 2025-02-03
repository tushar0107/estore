from django.contrib import admin

# Register your models here.

from .models import *
from django.contrib.auth.models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
admin.site.unregister(User)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user','phone','city','state']
    list_per_page = 20

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','brand','price']
    list_per_page = 20

class CartAdmin(admin.ModelAdmin):
    list_display = ['user','product']
    list_display_links = ['user','product']
    list_per_page = 20

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['user','product','quantity','date_ordered','total_amount','details','status']
    list_display_links = ['user','product']
    list_per_page = 20

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','total_price','payment_mode','payment_status','order_status']
    list_per_page = 20

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order','payment_method','transaction_id','payment_status']
    list_per_page = 20

class CustomerProfile(admin.StackedInline):
    model = Customer

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['first_name','last_name']
    inlines = (CustomerProfile,)

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Payment,PaymentAdmin)
admin.site.register(Cart,CartAdmin)
admin.site.register(Review)
admin.site.register(Category)
admin.site.register(OrderItem,OrderItemAdmin)
