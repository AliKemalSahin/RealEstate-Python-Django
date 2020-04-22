from django.contrib import admin

# Register your models here.
from django.utils.html import format_html
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin

from emlak.models import Category, Emlak, Images, Comment

class EmlakImageInLine(admin.TabularInline):   # image tablosundan 5 tane resim eklencek şekilde alan oluştur
    model = Images
    extra = 5   # galeri kaç resimden oluşsun?


class CategoryAdmin(admin.ModelAdmin): #admin panelinde hangi alanlar görülsün istiyorumun ayarı
    list_display = ['title','status','image_tag']   # title ile status gözüksün
    readonly_fields = ('image_tag',)
    list_filter = ['status']   # filtreleme sekmesi oluşturur statusa göre filtreler / altındaki şeylere göre evet hayır var bizde

class EmlakAdmin(admin.ModelAdmin):
    list_display = ['title','rooms','category','image_tag','status']
    readonly_fields = ('image_tag',)
    list_filter = ['status']
    inlines = [EmlakImageInLine]
    prepopulated_fields = {'slug': ('title',)}


class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title','emlak','image_tag']
    readonly_fields = ('image_tag',)

class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}    # slugın nereden oluştugunu belirttik

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Emlak,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Emlak,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'


class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject', 'comment', 'emlak', 'user', 'status']
    list_filter = ['status']


admin.site.register(Category,CategoryAdmin2)   # daha önce eklenen bi tablonun adminde gösterilmesi (category tablosu)
admin.site.register(Emlak,EmlakAdmin)   # daha önce eklenen bi tablonun adminde gösterilmesi
admin.site.register(Images,ImagesAdmin)
admin.site.register(Comment,CommentAdmin)