from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.

# CarModelInline class
class CarModelInline: 
    model = CarModel

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ("Make","Name", "Type", "Year")
    search_fields = ["Name"]

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ("Name, Description")
# Register models here
