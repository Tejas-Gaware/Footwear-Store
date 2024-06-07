from django.contrib import admin
from .models import Category, Customer, Contact, Cart, Payment, OrderPlaced, Product, ProductImage, ProductColor, ProductSize

# Register your models here.

admin.site.register(Category)
admin.site.register(Contact)

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'mobile',  'locality', 'city']
    
    
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity', 'color', 'total_cost']


@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'razorpay_order_id', 'razorpay_payment_status', 'razorpay_payment_id', 'paid']


@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'product', 'quantity', 'ordered_date', 'status', 'payment']


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage

class ProductColorAdmin(admin.StackedInline):
    model = ProductColor

class ProductSizeAdmin(admin.StackedInline):
    model = ProductSize


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin, ProductSizeAdmin, ProductColorAdmin]
    list_display = ['id', 'title', 'price']


admin.site.register(Product, ProductAdmin)

admin.site.register(ProductImage)
admin.site.register(ProductColor)
admin.site.register(ProductSize)
