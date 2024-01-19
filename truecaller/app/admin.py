from django.contrib import admin

from .models import Contact, GlobalContact, User

# Register your models here.
admin.site.register(User)
admin.site.register(Contact)
admin.site.register(GlobalContact)