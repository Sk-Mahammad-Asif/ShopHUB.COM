from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from app.models import ProductComment,UserOTP
from .models import (
    Customer,
    Product,
    Cart,
    OrderPlaced
)
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display=['id','user','name','locality','city','zipcode','state','profile_pic']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display=['id','title','selling_price','discounted_price','description','brand','category','product_image','product_image_child1','product_image_child2','product_image_child3','timestamp']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product','quantity']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display=['id','user','customer','customer_info','product','product_info','quantity','ordered_date','status']

    def customer_info(self,obj):
        link=reverse("admin:app_customer_change",args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>',link,obj.customer.name)
    
    def product_info(self,obj):
        link=reverse("admin:app_product_change",args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>',link,obj.product.title)

admin.site.register(ProductComment)
admin.site.register(UserOTP)
# Register your models here.
