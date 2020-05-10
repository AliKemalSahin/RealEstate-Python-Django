from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm, Select, TextInput, Textarea, FileInput
from django.urls import reverse
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):   # tablomuz
    STATUS = (            # --> 2 amaçla yapılır 1-Tabloyu oluşturmak   2- Adminde yönetilmeyi ayarlamak
        ('True','Evet'),
        ('False','Hayır'),
    )
    title = models.CharField(max_length=30)     # uzunluk
    keywords = models.CharField(blank=True,max_length=255)     # alan türü
    description = models.CharField(blank=True,max_length=255)     #alan türü
    image = models.ImageField(blank=True,upload_to='images/')     #dosya eklenecek resim
    status = models.CharField(max_length=10, choices=STATUS)   # yukarda evet hayır verdiğimiz için drowdown menude evet hayır var
    slug = models.SlugField(null=False, unique=True)     #adres satırında id yerine metinsel bir şekilde çagırmak icin category/3
    parent = TreeForeignKey('self',blank=True, null=True, related_name='children', on_delete=models.CASCADE)   # kendisiyle ilişkili(kendi id)
    create_at = models.DateTimeField(auto_now_add=True)   # ne zaman oluşturuldu
    update_at = models.DateTimeField(auto_now_add=True)   # ne zaman güncellendi

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])


    def image_tag(self):   # Adminde yuklenen resimlerin gosterilmesi
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))   # bu html kodu ile resimler gözüküyor
    image_tag.short_description = "Image"

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

class Emlak(models.Model):   # tablomuz
    STATUS = (                                                           # one to one -> user ın üye kaydı ve kimlik bilgisi
        ('True','Evet'),                                                   # many to one -> danışman ve öğrenci (her öğrencinin bir tane danışmanı vardır)
        ('False','Hayır'),                                               # many to many -> dersler ve öğrenciler
    )                                                                    # one to many -> pantolon hem kışlıkta hem erkek giysisi tablosunda olabilir
    category = models.ForeignKey(Category,on_delete=models.CASCADE)      # burada ise tablodaki gibi productta category_id category deki id ye bağlı(manyToOne)
    title = models.CharField(max_length=30)     # uzunluk
    keywords = models.CharField(blank=True,max_length=255)     # alan türü
    description = models.CharField(blank=True,max_length=255)     #alan türü
    image = models.ImageField(blank=True,upload_to='images/')     #dosya eklenecek resim
    price = models.FloatField()
    square = models.IntegerField()
    rooms = models.CharField(blank=True, max_length=5)
    salon = models.CharField(blank=True,max_length=20)
    yatakOda = models.CharField(blank=True, max_length=20)
    banyo = models.CharField(blank=True, max_length=20)
    garaj = models.CharField(blank=True, max_length=20)
    binaYasi = models.CharField(blank=True, max_length=20)
    detail = RichTextUploadingField()
    slug = models.SlugField(null=False, unique=True)
    status = models.CharField(max_length=10, choices=STATUS)   # yukarda evet hayır verdiğimiz için drowdown menude evet hayır var

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    create_at = models.DateTimeField(auto_now_add=True)   # ne zaman oluşturuldu
    update_at = models.DateTimeField(auto_now_add=True)   # ne zaman güncellendi

    def __str__(self):
        return self.title
    def image_tag(self):   # Adminde yuklenen resimlerin gosterilmesi
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))   # bu html kodu ile resimler gözüküyor
    image_tag.short_description = "Image"

    def get_absolute_url(self):
        return reverse('emlak_detail', kwargs={'slug': self.slug})

class EmlakForm(ModelForm):
    class Meta:
        model = Emlak
        fields = ['category','title','keywords','description','slug','image','price','square','rooms','salon','yatakOda','banyo','garaj','binaYasi','detail']
        widgets = {
            'category' : Select(attrs={'class': 'input', 'placeholder': 'category'}),
            'title' : TextInput(attrs={'class': 'input', 'placeholder': 'Başlık'}),
            'slug': TextInput(attrs={'class': 'input', 'placeholder': 'slug'}),
            'keywords' : TextInput(attrs={'class': 'input', 'placeholder': 'keywords'}),
            'description' : TextInput(attrs={'class': 'input', 'placeholder': 'description'}),
            'image' : FileInput(attrs={'class': 'input', 'placeholder': 'image'}),
            'price' : TextInput(attrs={'class': 'input', 'placeholder': 'Ücret'}),
            'square' : TextInput(attrs={'class': 'input', 'placeholder': 'Metre Kare'}),
            'rooms' : TextInput(attrs={'class': 'input', 'placeholder': 'Oda Sayısı'}),
            'salon' : TextInput(attrs={'class': 'input', 'placeholder': 'Salon Sayısı'}),
            'yatakOda' : TextInput(attrs={'class': 'input', 'placeholder': 'Yatak Oda Sayısı'}),
            'banyo' : TextInput(attrs={'class': 'input', 'placeholder': 'Banyo Sayısı'}),
            'garaj' : TextInput(attrs={'class': 'input', 'placeholder': 'Garaj Sayısı'}),
            'binaYasi' : TextInput(attrs={'class': 'input', 'placeholder': 'Bina Yaşı'}),
            'detail' : CKEditorWidget(),

        }


class Images(models.Model):
    emlak = models.ForeignKey(Emlak,on_delete=models.CASCADE)   # Cascade --> ilişkili oldugu(bağlı) emlak silinirse buda silinir demektir havada kalmasın diye
    title = models.CharField(max_length=50, blank=True) # blank= True null olabilir dedik                         # emlak id ile bağlamış olduk
    image = models.ImageField(blank=True, upload_to='images/')
    def __str__(self):
        return self.title   # bunu yapmazsak sitede object 1 2 diye gözükür ama title döndürerek imagein title i belli olmus olur
    def image_tag(self):   # Adminde yuklenen resimlerin gosterilmesi
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))   # bu html kodu ile resimler gözüküyor
    image_tag.short_description = "Image"


class Comment(models.Model):
    STATUS = (
        ('New', 'Yeni'),
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    emlak =models.ForeignKey(Emlak, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    comment = models.TextField(max_length=250, blank=True)
    rate = models.IntegerField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject','comment','rate']





