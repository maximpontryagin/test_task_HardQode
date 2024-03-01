from django.contrib import admin

from product.models import Group, Product


@admin.register(Product)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Group)
class CommentAdmin(admin.ModelAdmin):
    pass
