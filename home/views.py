from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from emlak.models import Emlak
from home.models import Setting,ContactFormu, ContactFormMessage


def index(request):
    setting = Setting.objects.get(pk=1)
    #text = "Merhaba Django !!!"                   # Ekrana bir şey yazdırma HttpResponse("text : %s" % text)
    #text = "Satış Danışmanı <br> Ali Kemal Şahin <br> Merhaba"
    #context = {'text': text}
    sliderdata = Emlak.objects.all()[:3] #gereksiz yere tüm veriyi getirmemek için :4 tane aldık

    context = {'setting': setting, 'page': 'home', 'sliderdata':sliderdata }
    return render(request, 'index.html', context)


def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'page': 'hakkimizda'}
    return render(request, 'hakkimizda.html', context)

def referanslar(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'page': 'hakkimizda'}
    return render(request, 'referanslarimiz.html', context)

def iletisim(request):

    if request.method == "POST":
        form = ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request,"Mesajınız Başarıyla Gönderilmiştir. Teşekkür Ederiz...")
            return HttpResponseRedirect ('/iletisim')


    setting = Setting.objects.get(pk=1)
    form = ContactFormu()
    context = {'setting': setting, 'form': form}
    return render(request, 'iletisim.html', context)