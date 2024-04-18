from django.contrib import admin
from .models import *
from django.utils.html import format_html

admin.site.site_header = 'Ogani Shop Admin Dashboard'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:70px; max-height:70px"/>'.format(obj.image.url))
    list_display = ('id', 'name', 'image_tag')
    list_filter = ('id', 'name')
    search_fields = ('name', 'id')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:70px; max-height:70px"/>'.format(obj.image.url))
    list_display = ('id', 'name', 'price', 'category', 'sale_off', 'image_tag')
    list_filter = ('id', 'name', 'category', 'sale_off')
    search_fields = ('id', 'name', 'category', 'sale_off')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'email')
    list_filter = ('id', 'user', 'name', 'email')
    search_fields = ('id', 'user', 'name', 'email')

@admin.register(Order)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'date_ordered', 'complete', 'transaction_id')
    list_filter = ('id', 'customer', 'date_ordered', 'complete', 'transaction_id')
    search_fields = ('id', 'customer', 'date_ordered', 'complete', 'transaction_id')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'order', 'quantity', 'date_added')
    list_filter = ('id', 'product', 'order', 'quantity', 'date_added')
    search_fields = ('id', 'product', 'order', 'quantity', 'date_added')

@admin.register(PurchaseHistory)
class CostumerPurchaseHistory(admin.ModelAdmin):
    list_display = ('customer', 'product', 'quantity', 'purchase_date')
    list_filter = ('customer', 'product', 'quantity', 'purchase_date')
    search_fields = ('customer', 'product', 'quantity', 'purchase_date')