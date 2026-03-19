from django.contrib import admin
from .models import Wall, Rack


class RackInline(admin.TabularInline):
    model = Rack
    extra = 4
    fields = ['code', 'description']


@admin.register(Wall)
class WallAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'rack_count', 'product_count', 'created_at']
    search_fields = ['name', 'category']
    inlines = [RackInline]


@admin.register(Rack)
class RackAdmin(admin.ModelAdmin):
    list_display = ['code', 'wall', 'product_count', 'created_at']
    list_filter = ['wall']
    search_fields = ['code', 'wall__name']
