from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from store.admin import ProductAdmin
from store.models import Product
from tags.models import TaggedItem
from core.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "email",
                    "first_name",
                    "last_name",
                ),
            },
        ),
    )


class TagInLine(GenericTabularInline):
    autocomplete_fields = ("tag",)
    model = TaggedItem
    extra = 0
    min_num = 1
    max_num = 10


class CustomProductAdmin(ProductAdmin):
    inlines = ProductAdmin.inlines + [TagInLine]


admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
