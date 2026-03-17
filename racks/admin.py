from django.contrib import admin
from .models import Rack, Shelf


class ShelfInline(admin.TabularInline):
    model = Shelf
    extra = 4
    fields = ['code', 'description']


@admin.register(Rack)
class RackAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'shelf_count', 'product_count', 'created_at']
    search_fields = ['name', 'category']
    inlines = [ShelfInline]


@admin.register(Shelf)
class ShelfAdmin(admin.ModelAdmin):
    list_display = ['code', 'rack', 'product_count', 'created_at']
    list_filter = ['rack']
    search_fields = ['code', 'rack__name']
