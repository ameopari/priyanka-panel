"""NewProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,include
from . import views
from .views import *
from Employee.views import *

urlpatterns = [
    path('',views.Home,name='home'),
    path('home',views.Base,name='home'),
    path('register',Register.as_view(),name='register'),
    path('login',Login.as_view(),name='login'),
    path('logout',Logout.as_view(),name='logout'),
    path('create',Create.as_view(),name='create'),
    path('show',views.show,name='show'),
    path('update/<int:id>',views.upd,name='upd'),
    path('delete/',views.delete,name='delete'),
    path('delete/<int:id>',views.delete,name='delete'),
    path('forgot',views.forgotPassword,name='forgot'),
    path('changepass/<int:code>',changePassword.as_view(),name='changepass'),
    path('product',Products.as_view(),name='product'),
    path('all-products',AllProduct.as_view(),name='listproduct'),
    path('edit/<int:id>',views.Edit,name='edit'),
    path('search',views.Search,name='search'),
    path('uedit',views.UserEdit,name='uedit'),
    path('settings', views.settings, name='settings'),
    path('settings/password', views.password, name='password'),
    # path('upduser',views.update_user_social_data)
  
    
]

