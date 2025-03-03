from django.shortcuts import render
from .models import Chemical
from django.http import JsonResponse

from django.core.serializers import serialize
# Create your views here.

def index(request):
    return JsonResponse({'status':'dfgkaja'})

def find_chemicals(request):    
    chemical = request.GET.get('chemical')
    queryset = list(Chemical.objects.filter(name__icontains=chemical))
    
    return JsonResponse({'status':True,'chemicals':serialize("json",queryset)})

def get_chemicals(request,id):
    result = Chemical.objects.get(pk = id)
    chemical = {
        'name':result.name,
        'description': result.description,
        'chemical_type': result.chemical_type,
        'lab_name': result.lab_name,
        'rack_no': result.rack_no,
        'image': result.image.url,
    }
    if(chemical is not None):
        return JsonResponse({'status':True,'chemical':chemical})
    return JsonResponse({'status':False,'message':'Selected chemical is not found'})

def add_chemicals(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        chemical_type = request.POST.get('chemical_type')
        lab_name = request.POST.get('lab_name')
        rack_no = request.POST.get('rack_no')
        image = request.FILES.get('image')
    
    chemical = Chemical.objects.create(name=name,description=description,chemical_type=chemical_type,lab_name=lab_name,rack_no=rack_no)
    
    try:
        chemical.image.save(image,save=False)
        chemical.save()
        return JsonResponse({'status':True,'message':'Chemical added'})
    except Exception as e:
        return JsonResponse({'status':False,'message':e})