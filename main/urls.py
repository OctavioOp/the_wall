from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('form', views.signin),
    path('logout',views.logout),
    path('login',views.login),
    path('create_message',views.post_message),
    path('delete/<id>', views.delete_message),
    path('create_comment/<id_m>',views.post_comment),
]
