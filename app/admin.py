from django.contrib import admin
from .models import CartItemModel, ProductModel, CategoryModel
# Register your models here.


admin.site.register(ProductModel)
admin.site.register(CartItemModel)
admin.site.register(CategoryModel)
