from django.contrib import admin

from orders.models import Order,Payment,OrderProduct

# Register your models here.


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('payment','user','product','quantity','product_price','ordered')
    extra =0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','order_number','full_name','phone','email','city','order_total','tax','status','is_ordered']
    list_filter = ['status','is_ordered']
    search_fields = ['order_number','first_name','last_name','phone','email']
    list_per_page = 20
    inlines = [OrderProductInline]

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['order','user','ordered','payment','created_at','updated_at']
    

admin.site.register(Order,OrderAdmin)
admin.site.register(Payment)
admin.site.register(OrderProduct,OrderProductAdmin)
