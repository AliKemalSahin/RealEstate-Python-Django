from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
from emlak.models import Category, Comment, EmlakForm, Emlak
from home.models import UserProfile
from user.forms import UserUpdateForm, ProfileUpdateForm


def index(request):
    category = Category.objects.all()
    current_user = request.user

    profile = UserProfile.objects.get(user_id = current_user.id)
    context = {'category': category,
               'profile': profile,
               }
    return render(request, 'user_profile.html', context)

def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance = request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Hesap Bilgilerin Başarıyla Güncellendi!')
            return redirect('/user')


    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'category' : category,
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'user_update.html', context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)
            messages.success(request, 'Şifreniz Başarıyla Değiştirildi.')
            return HttpResponseRedirect('/user/password')

        else:
            messages.error(request,'Lütfen Hatanızı Düzeltiniz.<br>' + str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request,'change_password.html', {
        'form': form, 'category': category
    })

@login_required(login_url='/login')
def comments(request):
    category = Category.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'comments': comments,
    }
    return render(request, 'user_comments.html', context)

@login_required(login_url='/login')
def deletecomment(request,id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()  # güvenlik açığını önlemek icin baştaki id yi alıyoruz
    messages.error(request, 'Yorumunuz Silindi.')
    return HttpResponseRedirect('/user/comments')

@login_required(login_url='/login')
def ilanVer(request):
    if request.method == 'POST':
        form = EmlakForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            data = Emlak()
            data.category = form.cleaned_data['category']
            data.user_id = current_user.id  # eklenmesi gerekebilir
            data.title = form.cleaned_data['title']
            data.slug = form.cleaned_data['slug']
            data.keywords = form.cleaned_data['keywords']
            data.description = form.cleaned_data['description']
            data.image = form.cleaned_data['image']
            data.price = form.cleaned_data['price']
            data.square = form.cleaned_data['square']
            data.rooms = form.cleaned_data['rooms']
            data.salon = form.cleaned_data['salon']
            data.yatakOda = form.cleaned_data['yatakOda']
            data.banyo = form.cleaned_data['banyo']
            data.garaj = form.cleaned_data['garaj']
            data.binaYasi = form.cleaned_data['binaYasi']
            data.detail = form.cleaned_data['detail']
            data.status = 'False'
            data.save()
            messages.success(request,'İlanınız Başarıyla Eklendi.')
            return HttpResponseRedirect('/user/ilanlarim')

        else:
            messages.success(request,'Hatalı Giriş : ' + str(form.errors))
            return HttpResponseRedirect('/user/ilanVer')

    else:
        category = Category.objects.all()
        form = EmlakForm()
        context = {
            'category' : category,
            'form' : form,
        }
        return  render(request, 'user_ilanVer.html', context)


@login_required(login_url='/login')
def ilanlarim(request):                 # hocada contents
    category = Category.objects.all()
    current_user = request.user
    ilanlar = Emlak.objects.filter(user_id = current_user.id)
    context = {
        'category' : category,
        'ilanlar' : ilanlar,
    }
    return render(request, 'user_ilanlarim.html',context)

@login_required(login_url='/login')
def ilanDuzenle(request,id):
    emlak = Emlak.objects.get(id=id)
    if request.method == 'POST':
        form = EmlakForm(request.POST, request.FILES, instance=emlak)
        if form.is_valid():
            form.save()
            messages.success(request,'İlanınız Başarıyla Güncellendi.')
            return HttpResponseRedirect('/user/ilanlarim')
        else:
            messages.success(request,'İçerik Hatası : '+ str(form.errors))
            return HttpResponseRedirect('/user/ilanDuzenle')

    else:
        category = Category.objects.all()
        form = EmlakForm(instance=emlak)
        context = {
            'category' : category,
            'form' : form,
        }
        return render(request,'user_ilanVer.html',context)
@login_required(login_url='/login')
def ilanSil(request, id):
    current_user = request.user
    Emlak.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request,'İlan Silindi!')
    return HttpResponseRedirect('/user/ilanlarim')












