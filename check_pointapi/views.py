import requests
from django.db import connection
from django.shortcuts import render, reverse
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password, make_password
def api_targets(request):
    if request.method == 'GET':
        # print(request.GET)
        with connection.cursor() as cursor:
            cursor.callproc('target_select')
            targets = dictfatchall(cursor)
        return JsonResponse(targets, safe=False)

def api_employees(request):
    if request.method == 'GET':
        # print(request.GET)
        with connection.cursor() as cursor:
            cursor.callproc('employee_select')
            employees = dictfatchall(cursor)
        return JsonResponse(employees, safe=False)

def api_subunits(request):
    if request.method == 'GET':
        # print(request.GET)
        with connection.cursor() as cursor:
            cursor.callproc('subunit_select')
            subunits = dictfatchall(cursor)
        return JsonResponse(subunits, safe=False)

def dictfatchall(cursor):
    columns = [col[0] for col in cursor.description]
    return[
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

@csrf_exempt
def api_orders(request, id_order=None):
    if not id_order:
        if request.method == 'GET':
            print(request.GET)
            in_datatime_begin = request.GET.get('in_datatime_begin',None)
            in_datatime_end = request.GET.get('in_datatime_end',None)
            id_subunit = request.GET.get('id_subunit',None)
            id_type_order = request.GET.get('id_type_order',None)
            id_employee = request.GET.get('id_employee',None)
            id_user = request.GET.get('id_user',None)
            id_target = request.GET.get('id_target',None)
            id_status = request.GET.get('id_status',None)

            in_datatime_begin = None if in_datatime_begin == '' else in_datatime_begin
            in_datatime_end = None if in_datatime_end == '' else in_datatime_end
            id_subunit = None if id_subunit == '' else id_subunit
            id_type_order = None if id_type_order == '' else id_type_order
            id_employee = None if id_employee == '' else id_employee
            id_user = None if id_user == '' else id_user
            id_target = None if id_target == '' else id_target
            id_status = None if id_status == '' else id_status
            with connection.cursor() as cursor:
                cursor.callproc('order_select_by_params', [in_datatime_begin, in_datatime_end, id_subunit, id_type_order, id_employee, id_user, id_target, id_status])
                orders = dictfatchall(cursor)
                return JsonResponse(orders, safe=False)
        elif request.method == 'POST':
            print(request.POST)
            in_datatime_begin_wish = request.POST.get('in_datatime_begin_wish')
            in_datatime_end_wish = request.POST.get('in_datatime_end_wish')
            in_group_number = request.POST.get('in_group_number', None)
            in_count_visitors = request.POST.get('in_count_visitors', 1)
            id_subunit = request.POST.get('id_subunit')
            id_type_order = request.POST.get('id_type_order')
            id_employee = request.POST.get('id_employee')
            id_user = request.POST.get('id_user')
            id_target = request.POST.get('id_target')
            id_status = request.POST.get('id_status', 1)
            if not in_datatime_begin_wish or not in_datatime_end_wish or not in_count_visitors or not id_subunit or not id_type_order or not id_employee or not id_user or not id_target or not id_status:
                return HttpResponse(status=400)
            with connection.cursor() as cursor:
                cursor.callproc('order_insert', [in_datatime_begin_wish, in_datatime_end_wish, in_group_number, in_count_visitors, id_subunit, id_type_order, id_employee, id_user, id_target, id_status])
                id_max_order = dictfatchall(cursor)
            return JsonResponse(id_max_order, safe=False)
        else:
            return HttpResponse(status=404)
    else:
        if request.method == 'GET':
            with connection.cursor() as cursor:
                cursor.callproc('order_select_by_id',[id_order])
                order = dictfatchall(cursor)
            return JsonResponse(order, safe=False)
        elif request.method == 'POST':
            print(request.POST)

            URL = request.build_absolute_uri(reverse('api_orders', kwargs= {'id_order': id_order}))
            print(URL)
            response = requests.get(URL)
            order = response.json()[0]
            print(order)

            in_number_order = request.POST.get('in_number_order', order['number_order'])
            in_datatime_begin_wish = request.POST.get('in_datatime_begin_wish', order['datatime_begin_wish'])
            in_datatime_end_wish = request.POST.get('in_datatime_end_wish', order['datatime_end_wish'])
            in_group_number = request.POST.get('in_group_number', order['group_number'])
            in_count_visitors = request.POST.get('in_count_visitors', order['count_visitors'])
            id_subunit = request.POST.get('id_subunit', order['subunit'])
            id_type_order = request.POST.get('id_type_order', order['type_order'])
            id_employee = request.POST.get('id_employee', order['employee'])
            id_user = request.POST.get('id_user', order['user'])
            id_target = request.POST.get('id_target', order['target'])
            id_status = request.POST.get('id_status', order['status'])

            in_datatime_begin = request.POST.get('in_datatime_begin', order['in_datatime_begin'])
            in_datatime_end = request.POST.get('in_datatime_end', order['in_datatime_end'])
            in_datatime_begin_checkpoint = request.POST.get('in_datatime_begin_checkpoint', order['in_datatime_begin_checkpoint'])
            in_datatime_end_checkpoint = request.POST.get('in_datatime_end_checkpoint', order['in_datatime_end_checkpoint'])
            in_datatime_begin_subunit = request.POST.get('in_datatime_begin_subunit', order['in_datatime_begin_subunit'])
            in_datatime_end_subunit = request.POST.get('in_datatime_end_subunit', order['in_datatime_end_subunit'])

            with connection.cursor() as cursor:
                cursor.callproc('order_update', [in_number_order, in_datatime_begin_wish, in_datatime_end_wish, in_group_number, in_count_visitors, id_subunit, id_type_order, id_employee, id_user, id_target, id_status, in_datatime_begin_checkpoint, in_datatime_end_checkpoint, in_datatime_begin_subunit, in_datatime_end_subunit])
            return HttpResponse(status=202)
        elif request.method == 'DELETE':
            return HttpResponse(status=202)
        else:
            return HttpResponse(status=404)
@csrf_exempt
def api_visitors(request):
    if request.method == 'GET':
        print(request.GET)
        id_order = request.GET.get('id_order',None)
        in_lfm = request.GET.get('in_lfm',None)
        in_passport = request.GET.get('in_passport',None)

        id_order = None if id_order == '' else id_order
        in_lfm = None if in_lfm == '' else in_lfm
        in_passport = None if in_passport == '' else in_passport
        with connection.cursor() as cursor:
            cursor.callproc('visitor_select',
                            [id_order,in_lfm,in_passport])
            visitor = dictfatchall(cursor)
        return JsonResponse(visitor, safe=False)
    elif request.method == 'POST':
        print(request.POST)
        in_lastname = request.POST.get('in_lastname')
        in_firstname = request.POST.get('in_firstname')
        in_email = request.POST.get('in_email')
        in_notice = request.POST.get('in_notice')
        in_date_of_birth = request.POST.get('in_date_of_birth')
        in_passport_series = request.POST.get('in_passport_series')
        in_passport_number = request.POST.get('in_passport_number')
        in_black_list_visit = request.POST.get('in_black_list_visit',0)
        if not in_lastname or not in_firstname or not in_email or not in_notice or not in_date_of_birth or not in_passport_series or not in_passport_number:
            return HttpResponse(status=400)
        in_middlename = request.POST.get('in_middlename', None)
        in_telephone_number = request.POST.get('in_telephone_number', None)
        in_organization = request.POST.get('in_organization', None)
        with connection.cursor() as cursor:
            cursor.callproc('visitor_insert',
                            [in_lastname, in_firstname, in_middlename, in_telephone_number, in_email, in_organization, in_notice, in_date_of_birth, in_passport_series, in_passport_number])
            visitors = dictfatchall(cursor)
        return JsonResponse(visitors, safe=False)
@csrf_exempt
def api_order_detail(request):
    if request.method == 'POST':
        id_last_order = request.POST.get('id_last_order')
        id_last_visitor = request.POST.get('id_last_visitor')
        in_black_list_visit_cause = request.POST.get('in_black_list_visit_cause', None)
        in_black_list_visit_cause = None if in_black_list_visit_cause == '' else in_black_list_visit_cause
        if not id_last_order or not id_last_visitor:
            return HttpResponse(status=400)
        with connection.cursor() as cursor:
            cursor.callproc('order_detail_insert',
                            [id_last_order, id_last_visitor, in_black_list_visit_cause])
            order_detail = dictfatchall(cursor)
        return JsonResponse(order_detail, safe=False)

@csrf_exempt
def api_user(request):
    if request.method == 'GET':
        print(request.GET)
        in_login = request.GET.get('in_login')
        in_password = request.GET.get('in_password')
        with connection.cursor() as cursor:
            cursor.callproc('user_select_by_login_password',
                            [in_login])
            user = dictfatchall(cursor)
        return JsonResponse(user, safe=False)
    elif request.method == 'POST':
        in_email = request.POST.get('in_email')
        in_password = request.POST.get('in_password')
        in_password = make_password(in_password , salt=None, hasher='default')
        in_login = request.POST.get('in_login', None)
        in_black_list_order = request.POST.get('in_black_list_order', 0)
        in_count_mist = request.POST.get('in_count_mist', 0)
        with connection.cursor() as cursor:
            cursor.callproc('user_insert',
                            [in_email, in_password, in_login, in_black_list_order, in_count_mist])
            return HttpResponse(status=202)