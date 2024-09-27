from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Department)
admin.site.register(Branch)
admin.site.register(Product)
admin.site.register(Image)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
 list_filter = ['c_name','branch']
 search_fields = ['c_name']