from django.shortcuts import render_to_response
from inspiration.models import *

def home(request):
    context = {
        "products" : list(Product.objects.all()),
        "colors" : list(set(list([p.color for p in Product.objects.all()])))
    }
    return render_to_response('index.html', context)

def plant_popup(request, plant_id):
    context = {
        "product": Product.objects.filter(id=plant_id)[0]
    }
    return render_to_response('plantpopup.html', context)
