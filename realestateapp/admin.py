from django.contrib import admin
from .models import User, Apartment
# Register your models here.
admin.site.register(Apartment)
admin.site.register(User)

# class ApartmentAdmin(admin.ModelAdmin):
#     list_display =
