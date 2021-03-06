"""emlakcilik URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from home import views

urlpatterns = [
    path('',include('home.urls')),   #hiç bir şey yazmadan home sayfası gelsin istersek
    path('hakkimizda/', views.hakkimizda, name ='hakkimizda'),
    path('referanslar/', views.referanslar, name='referanslar'),
    path('iletisim/', views.iletisim, name='iletisim'),
    path('home',include('home.urls')),
    path('emlak', include(('emlak.urls'))),
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('category/<int:id>/<slug:slug>/', views.category_products, name='category_products'),
    path('emlak/<int:id>/<slug:slug>/', views.emlak_detail, name='emlak_detail'),
    path('search/', views.emlak_search, name='emlak_search'),
    path('search_auto/', views.emlak_search_auto, name='emlak_search_auto'),
    path('logout/', views.logout_view, name='logout_view'),
    path('login/', views.login_view, name='login_view'),
    path('kayit/', views.kayit_view, name='kayit_view'),
    path('sss/', views.faq, name='faq'),



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   # Adminde yuklenen resimlerin gosterilmesine izin verilmesi
