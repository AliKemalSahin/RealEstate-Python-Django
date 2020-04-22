
from django.urls import path

from . import views

# ex:  /home/

urlpatterns = [
    path('',views.index, name='index'),
    path('/addcomment/<int:id>', views.addcomment, name='addcomment') # baştaki slash ı kaldırınca yorum yapma hata veriyor hocaya sor..


]