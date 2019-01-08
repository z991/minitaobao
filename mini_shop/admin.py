from django.contrib import admin

# Register your models here.
from .models import UserProfile, Product, Image

admin.site.register(UserProfile)
admin.site.register(Product)
admin.site.register(Image)