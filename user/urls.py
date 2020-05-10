
from django.urls import path

from . import views

# ex:  /home/

urlpatterns = [
    path('',views.index, name='index'),
    path('update/', views.user_update , name='user_update'),
    path('password/', views.change_password , name='change_password'),
    path('comments/', views.comments, name='comments'),
    path('deletecomment/<int:id>', views.deletecomment, name='deletecomment'),
    path('ilanVer/', views.ilanVer, name='ilanVer'),
    path('ilanlarim/', views.ilanlarim, name='ilanlarim'),
    path('ilanDuzenle/<int:id>', views.ilanDuzenle, name='ilanDuzenle'),
    path('ilanSil/<int:id>', views.ilanSil, name='ilanSil'),



]