from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from emlak.models import CommentForm,Comment


def index(request):
    return HttpResponse("Emlak Sayfasi")


@login_required(login_url='/login')  # login check

def addcomment(request,id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':   # form post edildiyse
        form = CommentForm(request.POST)
        if form.is_valid():
            current_user = request.user

            data = Comment()  # model ile bağlantı
            data.user_id = current_user.id
            data.emlak_id = id
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()   # veritabanına kayıt
            messages.success(request,'Yorumunuz başarı ile gönderilmiştir. Teşekkür Ederiz...')

            return HttpResponseRedirect(url)

    messages.warning(request, 'Yorumunuz kaydedilmedi.Lütfen Kontrol Ediniz!')
    return HttpResponseRedirect(url)











