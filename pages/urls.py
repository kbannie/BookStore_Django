from django.urls import path
from . import views

urlpatterns=[ #ip주소/
    path('',views.landing), #ip주소/
    path('about_me/',views.about_me), #ip주소/about_me/
    path('about_com/',views.about_com)
]