from django.contrib import admin
from .models import Product, MovementLog


class MovementLogInline(admin.TabularInline):
    model = MovementLog
    extra = 0
    readonly_fields = ['from_rack', 'from_shelf', 'to_rack', 'to_shelf', 'moved_by', 'moved_at']
    can_delete = False


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'category', 'rack', 'shelf', 'quantity', 'stock_status', 'updated_at']
    list_filter = ['rack', 'category', 'brand']
    search_fields = ['name', 'brand', 'category']
    list_editable = ['quantity']
    inlines = [MovementLogInline]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(MovementLog)
class MovementLogAdmin(admin.ModelAdmin):
    list_display = ['product', 'from_display', 'to_display', 'moved_by', 'moved_at']
    list_filter = ['moved_at']
    search_fields = ['product__name', 'product__brand']
    readonly_fields = ['moved_at']
