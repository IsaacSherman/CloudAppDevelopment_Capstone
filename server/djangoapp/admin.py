from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.

# CarModelInline class
class CarModelInline (admin.StackedInline): 
    model = CarModel
    

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ("Make", "Name", "Type", "Year")
    search_fields = ["Name"]
    list_filter=  ["Year"]


# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ("Name", "Description")

# Register models here
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)