"""adulis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/<int:id>/', views.product_detail, name='product_detail'),
    path('my_products/', views.my_products, name='my_products'),
    path('create_product/', views.create_product, name='create_product'),
    path('edit_product/<int:id>/', views.edit_product, name='edit_product'),
    path('profile/<slug:username>/', views.profile, name='profile'),
    path('^checkout/', views.create_purchase, name='create_purchase'),
    path('my_sellings/', views.my_sellings, name='my_sellings'),
    path('my_buyings/', views.my_buyings, name='my_buyings'),
    path(r'^category/(?P<link>[\w|-]+)/$', views.category, name='category'),
    path('search/', views.search, name='search'),
    path('sign_up/', views.sign_up, name="sign_up"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('search_page/', views.search_page, name='search_page')
]
