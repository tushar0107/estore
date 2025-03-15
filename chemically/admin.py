from django.contrib import admin
from .models import Chemical
from django.contrib.auth.models import *
# Register your models here.


class ChemicalAdmin(admin.ModelAdmin):
    list_display = ['name','lab_name','rack_no','chemical_type']


admin.site.register(Chemical,ChemicalAdmin)