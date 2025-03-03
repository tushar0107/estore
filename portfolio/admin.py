from django.contrib import admin
from .models import Myself
# Register your models here.

class MyselfAdmin(admin.ModelAdmin):
	list_display = ['my_email','subject']

admin.site.register(Myself,MyselfAdmin)