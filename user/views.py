from django.shortcuts import render, redirect
from home.models import *
from django.contrib.auth.hashers import PBKDF2PasswordHasher, Argon2PasswordHasher, BCryptPasswordHasher
from django.views.decorators.http import require_POST

def signup_login(request):
    mhomes = home.objects.all()[:3]
    
    result_login = ''
    if request.POST.get('btnLogIn'):
        
        hasher = Argon2PasswordHasher()
        email = request.POST.get('email_login')
        password = request.POST.get('password_login')
        password = hasher.encode(password, 'matkhau123123123')

        USER = user.objects.filter(email=email, password=password)
        if len(USER) > 0:
            USER_INFO = USER.values()[0]
            request.session['user_session'] = USER_INFO
            return redirect('home:index')
        else:
            result_login = """
            <div class="alert alert-danger" role="alert">
                There is something wrong with your email or password!
            </div>
            """


    result_register = ''
    if request.POST.get('btnSignUp'):
        
        hasher = Argon2PasswordHasher()
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password = hasher.encode(password, 'matkhau123123123')

        USER = user(name = name, email = email, password = password)
        USER.save()
        
        result_register = """
            <div class="alert alert-success" role="alert">
                New account created successfully!
            </div>
        """
       
    return render(request, 'register.html', context={
        'result_register':  result_register,  
        'result_login': result_login,
        'mhomes':mhomes,
    })

def log_out(request):
    if 'user_session' in request.session:
        del request.session['user_session']
    return redirect('user:signup_login')


def profile(request):
    mhomes = home.objects.all()[:3]
    
    USER_current = user.objects.filter(email = request.session.get('user_session')['email'])
    request.session.get('user_session')['name'] = USER_current.values()[0]['name']
    request.session.get('user_session')['phone'] = USER_current.values()[0]['phone']
    request.session.get('user_session')['address'] = USER_current.values()[0]['address']
    request.session.get('user_session')['description'] = USER_current.values()[0]['description']
    request.session.get('user_session')['image'] = USER_current.values()[0]['image']

    result_update = ""
    if request.POST.get('btnUpdateInfo'):
        USER = user.objects.get(email = request.session.get('user_session')['email'])
        USER.name = request.POST.get('name')
        USER.phone = request.POST.get('phone')
        USER.address = request.POST.get('address')
        USER.description = request.POST.get('description')
        if len(request.FILES) > 0:
            USER.image = request.FILES['image']
        USER.save()

        request.session.get('user_session')['name'] = USER.name
        request.session.get('user_session')['phone'] = USER.phone
        request.session.get('user_session')['address'] = USER.address
        request.session.get('user_session')['description'] = USER.description
        request.session.get('user_session')['image'] = USER.image

        result_update = """
            <div class="alert alert-success" role="alert">
                Update information successfully!
            </div>
        """

    return render(request, 'profile.html', context={
        'result_update':result_update,
        'user':USER_current[0],
        'mhomes':mhomes,
    })

def user_properties(request):
    mhomes = home.objects.all()[:3]

    homes = home.objects.filter(owner=request.session.get('user_session')['id'])
    thumbnails = []
    for each in homes:
        thumbnails.append(Image.objects.filter(home=each.id).first())

    return render(request, 'user-properties.html', context={
        'homes':homes,
        'thumbnails':thumbnails,
        'mhomes':mhomes,
    })

def submit(request):
    mhomes = home.objects.all()[:3]
    if request.POST.get('btnSubmit'):
        new_home = home()
        new_home.name = request.POST.get('name')
        new_home.price = request.POST.get('price')
        new_home.area = request.POST.get('area')
        new_home.bedrooms = request.POST.get('bedrooms')
        new_home.bathrooms = request.POST.get('bathrooms')
        new_home.garden = request.POST.get('garden')
        new_home.garage = request.POST.get('garage')
        new_home.description = request.POST.get('description')
        USER = user.objects.get(email=request.session.get('user_session')['email'])
        new_home.owner = USER
        new_home.save()

        HOME = home.objects.all().last()
        if len(request.FILES.getlist('images')) > 0:
            for each in request.FILES.getlist('images'):
                image = Image()
                image.home = HOME
                image.image = each
                image.save()

        HOME.thumbnail = request.FILES.getlist('images')[0]
        HOME.save()
        return redirect('user:user_properties')
        
    return render(request, 'submit.html', context={
        'mhomes':mhomes,
    })

