from django.db import models

# Create your models here.
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):   # tablomuz
    STATUS = (            # --> 2 amaçla yapılır 1-Tabloyu oluşturmak   2- Adminde yönetilmeyi ayarlamak
        ('True','Evet'),
        ('False','Hayır'),
    )
    title = models.CharField(max_length=30)     # uzunluk
    keywords = models.CharField(max_length=255)     # alan türü
    description = models.CharField(max_length=255)     #alan türü
    image = models.ImageField(blank=True,upload_to='images/')     #dosya eklenecek resim
    status = models.CharField(max_length=10, choices=STATUS)   # yukarda evet hayır verdiğimiz için drowdown menude evet hayır var
    slug = models.SlugField()     #adres satırında id yerine metinsel bir şekilde çagırmak icin category/3
    parent = models.ForeignKey('self',blank=True, null=True, related_name='children', on_delete=models.CASCADE)   # kendisiyle ilişkili(kendi id)
    create_at = models.DateTimeField(auto_now_add=True)   # ne zaman oluşturuldu
    update_at = models.DateTimeField(auto_now_add=True)   # ne zaman güncellendi

    def __str__(self):
        return self.title
    def image_tag(self):   # Adminde yuklenen resimlerin gosterilmesi
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))   # bu html kodu ile resimler gözüküyor
    image_tag.short_description = "Image"

class Emlak(models.Model):   # tablomuz
    STATUS = (                                                           # one to one -> user ın üye kaydı ve kimlik bilgisi
        ('True','Evet'),                                                   # many to one -> danışman ve öğrenci (her öğrencinin bir tane danışmanı vardır)
        ('False','Hayır'),                                               # many to many -> dersler ve öğrenciler
    )                                                                    # one to many -> pantolon hem kışlıkta hem erkek giysisi tablosunda olabilir
    category = models.ForeignKey(Category,on_delete=models.CASCADE)      # burada ise tablodaki gibi productta category_id category deki id ye bağlı(manyToOne)
    title = models.CharField(max_length=30)     # uzunluk
    keywords = models.CharField(max_length=255)     # alan türü
    description = models.CharField(max_length=255)     #alan türü
    image = models.ImageField(blank=True,upload_to='images/')     #dosya eklenecek resim
    price = models.FloatField()
    square = models.IntegerField()
    rooms = models.CharField(max_length=5)
    detail = RichTextUploadingField()
    status = models.CharField(max_length=10, choices=STATUS)   # yukarda evet hayır verdiğimiz için drowdown menude evet hayır var

    create_at = models.DateTimeField(auto_now_add=True)   # ne zaman oluşturuldu
    update_at = models.DateTimeField(auto_now_add=True)   # ne zaman güncellendi

    def __str__(self):
        return self.title
    def image_tag(self):   # Adminde yuklenen resimlerin gosterilmesi
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))   # bu html kodu ile resimler gözüküyor
    image_tag.short_description = "Image"

class Images(models.Model):
    emlak = models.ForeignKey(Emlak,on_delete=models.CASCADE)   # Cascade --> ilişkili oldugu(bağlı) emlak silinirse buda silinir demektir havada kalmasın diye
    title = models.CharField(max_length=50, blank=True) # blank= True null olabilir dedik                         # emlak id ile bağlamış olduk
    image = models.ImageField(blank=True, upload_to='images/')
    def __str__(self):
        return self.title   # bunu yapmazsak sitede object 1 2 diye gözükür ama title döndürerek imagein title i belli olmus olur
    def image_tag(self):   # Adminde yuklenen resimlerin gosterilmesi
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))   # bu html kodu ile resimler gözüküyor
    image_tag.short_description = "Image"