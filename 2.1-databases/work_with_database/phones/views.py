from django.shortcuts import render, redirect
from .models import Phone

def index(request):
    return redirect('catalog')


def show_catalog(request):
    sort = request.GET.get('sort', 'id')
    phone_info = Phone.objects.all().order_by('id')
    if sort == 'name':
        phone_info = Phone.objects.all().order_by('name')
    elif sort == 'min_price':
        phone_info = Phone.objects.all().order_by('price')
    elif sort == 'max_price':
        phone_info = Phone.objects.all().order_by('-price')
    template = 'catalog.html'
    context = {'phones': phone_info}
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    context = {'phone': Phone.objects.get(slug=slug)}
    return render(request, template, context)
