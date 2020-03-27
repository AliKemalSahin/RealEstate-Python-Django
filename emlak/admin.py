from django.contrib import admin

# Register your models here.
from emlak.models import Category, Emlak, Images

class EmlakImageInLine(admin.TabularInline):   # image tablosundan 5 tane resim eklencek şekilde alan oluştur
    model = Images
    extra = 5   # galeri kaç resimden oluşsun?


class CategoryAdmin(admin.ModelAdmin): #admin panelinde hangi alanlar görülsün istiyorumun ayarı
    list_display = ['title','status','image_tag']   # title ile status gözüksün
    readonly_fields = ('image_tag',)
    list_filter = ['status']   # filtreleme sekmesi oluşturur statusa göre filtreler / altındaki şeylere göre evet hayır var bizde

class EmlakAdmin(admin.ModelAdmin):
    list_display = ['title','rooms','detail','image_tag','status']
    readonly_fields = ('image_tag',)
    list_filter = ['status']
    inlines = [EmlakImageInLine]


class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title','emlak','image_tag']
    readonly_fields = ('image_tag',)

admin.site.register(Category,CategoryAdmin)   # daha önce eklenen bi tablonun adminde gösterilmesi (category tablosu)
admin.site.register(Emlak,EmlakAdmin)   # daha önce eklenen bi tablonun adminde gösterilmesi
admin.site.register(Images,ImagesAdmin)