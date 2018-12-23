from django.contrib import admin
from django.urls import path
from . import views

app_name = 'xtcheat'
urlpatterns = [
    path('login/',views.login,name='login'),
    path('person/',views.personalset,name='personal'),
    # path('hello/',views.test,name='test')
    path('update_phone/',views.update_phone,name='update_phone'),
    path('send_phone_validatenum/',views.send_phone_validatenum,name='send_phone_validatenum'),
    path('save_phone/',views.save_phone,name='save_phone'),
    path('update_email/',views.update_email,name='update_email'),
    path('save_email/',views.save_email,name='save_email'),
    path('send_email_validatenum/',views.send_email_validatenum,name="send_email_validatenum"),
    path('change_phoneon/',views.change_phoneon,name='chang_phoneon'),
    path('change_emailon/',views.change_emailon,name='change_emailon'),
    path('get_info_via_cookies/',views.get_info_via_cookies),
    path('wait/',views.wait,name='wait'),
]