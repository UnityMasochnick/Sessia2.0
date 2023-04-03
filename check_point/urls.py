"""check_point URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from check_pointapi import views as views_api
from check_pointapp import views as views_app
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api_orders/<id_order>', views_api.api_orders, name='id_order/<id_order>'),
    path('api_orders', views_api.api_orders, name='api_orders'),
    path('api_visitors', views_api.api_visitors, name='api_visitors'),
    path('api_user', views_api.api_user, name='api_user'),
    path('', views_app.main, name='main'),
    path('order_add', views_app.order_add, name='order_add'),
    path('orders', views_app.orders, name='orders'),
    path('signup', views_app.signup, name='signup'),
    path('login', views_app.login, name='login'),
    path('api_targets', views_api.api_targets, name='api_targets'),
    path('api_order_detail', views_api.api_order_detail, name='api_order_detail'),
    path('api_employees', views_api.api_employees, name='api_employees'),
    path('api_subunits', views_api.api_subunits, name='api_subunits'),

]
