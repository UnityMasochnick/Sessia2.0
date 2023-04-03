import datetime

import requests
from django.contrib.auth.hashers import check_password
from django.core.files.images import ImageFile
from django.core.files.storage import default_storage
from django.db import connection
from django.shortcuts import render, reverse, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os

from check_point import settings


def main(request):
    template ='check_pointapp/main.html'
    context = {}
    return render(request,template, context)

def order_add(request):
    template = 'check_pointapp/order_add.html'
    context = {}
    URL = request.build_absolute_uri(reverse('api_targets'))
    URL2 = request.build_absolute_uri(reverse('api_employees'))
    URL3 = request.build_absolute_uri(reverse('api_subunits'))
    response = requests.get(URL).json()
    response2 = requests.get(URL2).json()
    response3 = requests.get(URL3).json()
    context['targets'] = response
    context['employees'] = response2
    context['subunits'] = response3

    date_begin = datetime.date.today()+datetime.timedelta(days=1)
    date_end = datetime.date.today()+datetime.timedelta(days=15)
    min_date_of_birth = datetime.date.today() - datetime.timedelta(days=5840)
    context['date_begin'] = date_begin.__str__()
    context['date_end'] = date_end.__str__()
    context['min_date_of_birth'] = min_date_of_birth.__str__()
    if 'order_insert' in request.POST:
        data = dict(request.POST)
        data['id_type_order'] = 2
        data['id_user'] = 2
        print(data)
        URL = request.build_absolute_uri(reverse('api_orders'))
        response_orders = requests.post(URL, data=data)
        order_adds = response_orders.json()[0]
        id_last_order = order_adds.get('id_last_order')
        print(id_last_order)

        URL = request.build_absolute_uri(reverse('api_visitors'))
        response_visitors = requests.post(URL, data=data)
        visitor_adds = response_visitors.json()[0]
        id_last_visitor = visitor_adds.get('id_last_visitor')
        print(id_last_visitor)

        photo_file = request.FILES.get('in_photo')
        photo_file_name = photo_file.name
        photo_file_r = photo_file_name.split('.')[-1]
        photo_file_name = f"{id_last_visitor}.{photo_file_r}"
        path = os.path.join(settings.MEDIA_ROOT, 'photos', photo_file_name)
        default_storage.save(path, photo_file)
        with open(path, mode='rb') as f:
            photo_file = ImageFile(f)
            photo_file_width = photo_file.width
            photo_file_height = photo_file.height
            photo_file_size = photo_file.size
            print(photo_file_width, ' ', photo_file_height, ' ', photo_file_size)
        if photo_file_width/photo_file_height == 0.75:
            if photo_file_size > 4194304:
                return HttpResponse('<h3>Фото слишком большого размера!</h3>')

        else:
            return HttpResponse('<h3>Фото не 3:4!</h3>')


        passport_scan_file = request.FILES.get('in_passport_scan')
        passport_scan_file_name = passport_scan_file.name
        passport_scan_file_r = passport_scan_file_name.split('.')[-1]
        passport_scan_file_name = f"{id_last_visitor}.{passport_scan_file_r}"
        path = os.path.join(settings.MEDIA_ROOT, 'passports', photo_file_name)
        default_storage.save(path, passport_scan_file)

        data = {'id_last_order': id_last_order,
                'id_last_visitor': id_last_visitor,
                'in_black_list_visit_cause': None}
        print(data)
        URL = request.build_absolute_uri(reverse('api_order_detail'))
        response_order_detail = requests.post(URL, data=data)
         # снимаю данные с полей, вызов урла
    return render(request, template, context)

def orders(request):
    template = 'check_pointapp/orders.html'
    context = {}
    URL = request.build_absolute_uri(reverse('api_orders'))
    id_user = 1  # достаём из куки
    params = {'id_user': id_user}
    response_orders = requests.get(URL, params).json()
    for order in response_orders:
        dt = order['datatime_begin_wish'].split('T')
        order['date'] = dt[0]
        order['time'] = dt[1]
    context['orders'] = response_orders
    return render(request, template, context)

def login(request):
    template = 'check_pointapp/login.html'
    context = {}

    if 'signin' in request.POST:
        params = request.POST
        URL = request.build_absolute_uri(reverse('api_user'))
        response_user = requests.get(URL, params=params).json()
        if len(response_user)!=0:
            response_user = response_user[0]
            print('----------------------')
            print(response_user)
            print('----------------------')
            in_password = request.POST.get('in_password')
            in_login = request.POST.get('in_login')

            if not check_password(in_password, response_user.get('password')):
                return HttpResponse('<h3>Неверный пароль<h3>')
            else:
            # if in_password == response_user.get('password'):
                request.session['appuser'] = response_user
                print("Сессия:")
                print(request.session['appuser'])
                print(request.session)
                return redirect(to='main')
            # else:
            #      return HttpResponse('<h3>Неверный пароль<h3>')
        else:
                return HttpResponse('<h3>Такого логина не существует<h3>')

    return render(request, template, context)

def signup(request):
    template = 'check_pointapp/signup.html'

    context = {}
    URL = request.build_absolute_uri(reverse('api_user'))
    data = request.POST
    response_user = requests.post(URL, data=data)
    if 'registration' in request.POST:
        return redirect(to='login')
    return render(request, template, context)



# Create your views here.
