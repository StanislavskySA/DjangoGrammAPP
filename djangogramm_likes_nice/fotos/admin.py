from django.contrib import admin

from .models import Fotos, Like, Follow

# Register your models here.

admin.site.register(Fotos)
admin.site.register(Like)
admin.site.register(Follow)
