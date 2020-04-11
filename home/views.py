from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from emlak.models import Emlak, Category
from home.models import Setting,ContactFormu, ContactFormMessage


def index(request):
    setting = Setting.objects.get(pk=1)
    #text = "Merhaba Django !!!"                   # Ekrana bir şey yazdırma HttpResponse("text : %s" % text)
    #text = "Satış Danışmanı <br> Ali Kemal Şahin <br> Merhaba"
    #context = {'text': text}
    sliderdata = Emlak.objects.all()[:3] #gereksiz yere tüm veriyi getirmemek için :4 tane aldık
    category = Category.objects.all()
    dayproducts = Emlak.objects.all()[:4]
    lastproducts = Emlak.objects.all().order_by('-id')[:4]
    onecikan = Emlak.objects.all().order_by('?')[:4]

    context = {'setting': setting,'category': category, 'page': 'home', 'sliderdata':sliderdata,
               'dayproducts':dayproducts,'lastproducts':lastproducts,'onecikan':onecikan, }
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



def category_products(request,id,slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    emlaklar = Emlak.objects.filter(category_id=id)
    context = {'emlaklar':emlaklar,'category':category,'categorydata':categorydata}
    return render(request,'emlaklar.html',context)