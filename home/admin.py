from django.contrib import admin

from home.models import Setting, ContactFormMessage, UserProfile, FAQ


class ContactFormMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject','message','note', 'status']
    list_filter = ['status']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'phone', 'adress', 'city', 'country', 'image_tag']


class FAQAdmin(admin.ModelAdmin):
    list_display = ['ordernumber','question', 'answer','status']
    list_filter = ['status']


admin.site.register(ContactFormMessage,ContactFormMessageAdmin)
admin.site.register(Setting)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(FAQ, FAQAdmin)
