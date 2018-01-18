# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from queriesapp.models import Seller_details, Product_details, Orders

class SellerAdmin(admin.ModelAdmin):
    list_display = ('name','number','address','date')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','product_quantity','product_price','seller')

class OrdersAdmin(admin.ModelAdmin):
    list_display = ('order_name','order_quantity','seller_name','buyer_name','buyer_address','order_date')



admin.site.register(Orders,OrdersAdmin)
admin.site.register(Seller_details,SellerAdmin)
admin.site.register(Product_details,ProductAdmin)
