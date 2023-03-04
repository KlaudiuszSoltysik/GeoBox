from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),  
    path('set-new-password/<uidb64>/<token>/', views.set_new_password, name='set_new_password'),  
    path('reset-password', views.reset_password, name='reset_password'),  
]