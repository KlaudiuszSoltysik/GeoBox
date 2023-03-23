from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),  
    path('set-new-password/<uidb64>/<token>/', views.set_new_password, name='set_new_password'),  
    path('reset-password', views.reset_password, name='reset_password'),
    path('log-out', views.log_out, name='log_out'),
    path('reset-filters', views.reset_filters, name='reset_filters'),
    path('boxes', views.boxes, name='boxes'),
    path('add-box', views.add_box, name='add_box'),
    path('get-suggestions/<str:input>', views.get_suggestions, name='get_suggestions'),
    path('delete-comment/<int:id>', views.delete_comment, name='delete_comment'),
    path('delete-box/<int:id>', views.delete_box, name='delete_box'),
    path('box/<int:id>', views.box, name='box'),
    path('account', views.account, name='account'),
    path('edit-comment/<int:id>', views.edit_comment, name='edit_comment'),
    path('edit-box/<int:id>', views.edit_box, name='edit_box'),
]