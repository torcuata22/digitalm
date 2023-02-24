from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:id>', views.detail, name='detail'),
    path('success/', views.payment_success_view, name='success'),
    path('failed/', views.payment_failed_view, name='failed'),
    path('api/checkout-session/<int:id>/',views.create_checkout_session,name='api_checkout_session'),
    path('createproduct/',views.create_product,name='createproduct'),
    path('editproduct/<int:id>/',views.product_edit,name='editproduct'),
    path('delete/<int:id>/',views.product_delete,name='delete'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('register/',views.register,name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='myapp/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='myapp/logout.html'),name='logout'),

]