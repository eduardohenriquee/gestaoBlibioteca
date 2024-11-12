from django.contrib import admin
from django.urls import path, include
from contas import views as contas_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('products.urls')),
    path('', contas_views.login_view, name='login'),
    path('register/', contas_views.criar_usuario, name='register'),
    path('logout/', contas_views.login_view, name='logout'),
]