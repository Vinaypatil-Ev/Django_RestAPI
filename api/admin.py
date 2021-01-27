from django.contrib import admin

# Register your models here.

from .models import Blog

# admin.site.register(Blog)

@admin.register(Blog)
class BlogModel(admin.ModelAdmin):
    list_filter = ["title", "desc"]
    list_display = ["title", "desc"]

