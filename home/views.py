from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from home.models import Setting


def index(request):
    setting = Setting.objects.get(pk=1)
    #text = "Merhaba Django !!!"                   # Ekrana bir şey yazdırma HttpResponse("text : %s" % text)
    #text = "Satış Danışmanı <br> Ali Kemal Şahin <br> Merhaba"
    #context = {'text': text}

    context = {'setting': setting}
    return render(request, 'index.html', context)
