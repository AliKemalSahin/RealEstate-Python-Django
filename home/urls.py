from django.urls import path

from . import views

# ex:  /home/

urlpatterns = [
    path('',views.index, name='index'),


]