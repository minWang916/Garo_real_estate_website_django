from django.shortcuts import render, redirect
from home.models import *


def delete(request, id):

    HOME = home.objects.get(id = id).delete()

    return redirect('user:user_properties')

def edit(request, id):

    single_home = home.objects.get(id = id)

    if request.POST.get('btnEdit'):
        single_home.name = request.POST.get('name')
        single_home.price = request.POST.get('price')
        single_home.area = request.POST.get('area')
        single_home.bedrooms = request.POST.get('bedrooms')
        single_home.bathrooms = request.POST.get('bathrooms')
        single_home.garden = request.POST.get('garden')
        single_home.garage = request.POST.get('garage')
        single_home.description = request.POST.get('description')

        if len(request.FILES.getlist('images')) > 0:
            for each in request.FILES.getlist('images'):
                image = Image()
                image.home = single_home
                image.image = each
                image.save()
            
            single_home.thumbnail = request.FILES.getlist('images')[0]
        
        single_home.save()
        return redirect('user:user_properties')

    return render(request, 'edit.html', context={
        'single':single_home,
    })

def search(request):

    homes = home.objects.all()
    mhomes = home.objects.all()[:3]
    recommend_homes = homes[:4]
    keyword = ""
    
    if request.GET.get("home_search"):
        keyword = request.GET.get("home_search")
        homes = home.objects.filter(name__contains = keyword)

    return render(request, 'homes.html', context={
        'homes':homes,
        'r_homes':recommend_homes,
        'mhomes':mhomes,
        'keyword':keyword,
    })
    

def index(request):

    mhomes = home.objects.all()[:3]

    homes = home.objects.all()[:7]
    amount_homes = len(home.objects.all())
    amount_owners = len(user.objects.all())

    return render(request, 'index.html', context={
        'amount_homes':amount_homes,
        'homes':homes,
        'amount_owners':amount_owners,
        'mhomes':mhomes,
    })


def contact(request):
    mhomes = home.objects.all()[:3]
    return render(request, 'contact.html', context={
        'mhomes':mhomes,
    })

def homes(request):
    mhomes = home.objects.all()[:3]
    homes = home.objects.all()
    recommend_homes = homes[:4]

    return render(request, 'homes.html', context={
        'homes':homes,
        'r_homes':recommend_homes,
        'mhomes':mhomes,
    })

def register(request):
    mhomes = home.objects.all()[:3]
    return render(request, 'register.html', context={
        'mhomes':mhomes,
    })

def property_single(request, id):
    mhomes = home.objects.all()[:3]

    HOME = home.objects.get(id = id)
    OWNER = user.objects.get(id = HOME.owner.id)
    PHOTOS = Image.objects.filter(home = HOME.id)
    return render(request, 'home.html', context={
        'photos':PHOTOS,
        'owner':OWNER,
        'property_single':HOME,
        'mhomes':mhomes,
    })




