from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from home.forms import SearchForm, KayitForm
# Create your views here.
from emlak.models import Emlak, Category, Images, Comment
from home.models import Setting, ContactFormu, ContactFormMessage, UserProfile, FAQ
import json

def index(request):
    setting = Setting.objects.get(pk=1)
    #text = "Merhaba Django !!!"                   # Ekrana bir şey yazdırma HttpResponse("text : %s" % text)
    #text = "Satış Danışmanı <br> Ali Kemal Şahin <br> Merhaba"
    #context = {'text': text}
    sliderdata = Emlak.objects.all()[:3] #gereksiz yere tüm veriyi getirmemek için :4 tane aldık
    category = Category.objects.all()

    dayproducts = Emlak.objects.filter(status='True')
    lastproducts = Emlak.objects.filter(status='True').order_by('-id')[:4]
    onecikan = Emlak.objects.filter(status='True').order_by('?')[:4]

    context = {'setting': setting,'category': category, 'page': 'home', 'sliderdata':sliderdata,
               'dayproducts':dayproducts,'lastproducts':lastproducts,'onecikan':onecikan, }
    return render(request, 'index.html', context)


def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting,'category': category, 'page': 'hakkimizda'}
    return render(request, 'hakkimizda.html', context)

def referanslar(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting,'category': category, 'page': 'hakkimizda'}
    return render(request, 'referanslarimiz.html', context)

def iletisim(request):
    category = Category.objects.all()
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
    context = {'setting': setting,'category': category, 'form': form}
    return render(request, 'iletisim.html', context)



def category_products(request,id,slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    emlaklar = Emlak.objects.filter(category_id=id, status='True')
    context = {'emlaklar':emlaklar,'category':category,'categorydata':categorydata}
    return render(request,'emlaklar.html',context)


def emlak_detail(request,id,slug):
    category = Category.objects.all()
    emlak = Emlak.objects.get(pk=id)
    images = Images.objects.filter(emlak_id=id)
    comments = Comment.objects.filter(emlak_id=id,status='True')

    context = {'emlak':emlak,
               'category':category,
               'images':images,
               'comments': comments,
               }
    return render(request,'emlak_detail.html',context)

def emlak_search(request):
    if request.method == 'POST':  #form post edildiyse
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()

            catid = form.cleaned_data['catid']
            query = form.cleaned_data['query']

            if catid == 0:
                emlaklar = Emlak.objects.filter(title__icontains=query, status='True') # select * from product where title like %query% demek, icontain büyük kücük ayretmez
            else:
                emlaklar = Emlak.objects.filter(title__icontains=query, category_id=catid, status='True')


            context = {'emlaklar': emlaklar,
                       'category': category,
                       }
            return render(request, 'emlak_search.html', context)

    return HttpResponseRedirect('/')

def emlak_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        emlak = Emlak.objects.filter(title__icontains=q,status='True')
        results = []
        for rs in emlak:
            emlak_json = {}
            emlak_json = rs.title
            results.append(emlak_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request,"Giriş Hatası. Kullanıcı Adı veya Şifreniz Hatalı !")
            return HttpResponseRedirect('/login')

    category = Category.objects.all()
    context = {'category': category, }
    return render(request, 'login.html', context)


def kayit_view(request):
    if request.method == 'POST':
        form = KayitForm(request.POST)
        if form.is_valid():      # burda if else yapmamıza gerek yok zaten kaydedilen yollanıyor.Validation yapılıyor burda.
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "images/users/user.png"
            data.save()

            return HttpResponseRedirect('/')

    form = KayitForm()
    category = Category.objects.all()
    context = {'category': category,
               'form': form,
               }
    return render(request, 'kayit.html', context)


def faq(request):
    category = Category.objects.all()
    faq = FAQ.objects.all().order_by('ordernumber')
    context = {
        'category':category,
        'faq':faq
    }
    return render(request,'faq.html',context)