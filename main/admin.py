from django.contrib import admin
from .models import *

admin.site.register(Brand)
admin.site.register(Size)

class BannerAdmin(admin.ModelAdmin):
    list_display = ('alt_text', 'image_tag')
admin.site.register(Banner, BannerAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_tag')
admin.site.register(Category, CategoryAdmin)

class ColorAdmin(admin.ModelAdmin):
    list_display = ('title', 'color_tag')
admin.site.register(Color, ColorAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'brand', 'status', 'featured')
    list_editable = ('status', 'featured')
admin.site.register(Product, ProductAdmin)

class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'price', 'color', 'size', 'image_tag')
admin.site.register(ProductAttribute, ProductAttributeAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_editable = ('paid_status', 'order_status')
    list_display = ('user', 'total_amount', 'paid_status', 'order_date', 'order_status')
admin.site.register(Order, OrderAdmin)

class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'item', 'image_tag', 'qty', 'price', 'total')
admin.site.register(OrderItems, OrderItemsAdmin)

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'review_text', 'get_rating')
admin.site.register(ProductReview, ProductReviewAdmin)


admin.site.register(Wishlist)

class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'status')
admin.site.register(Address, AddressAdmin)

