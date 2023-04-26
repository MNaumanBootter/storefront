from django.contrib import admin
from store import models
from django.db.models import Count
from django.utils.html import format_html
from django.utils.http import urlencode
from django.urls import reverse

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "unit_price", "inventory_status", "collection_title")
    list_editable = ("unit_price",)
    list_per_page = 10
    list_select_related = ("collection",)

    @admin.display(ordering="collection")
    def collection_title(self, product: models.Product) -> str:
        return product.collection.title

    @admin.display(ordering="inventory")
    def inventory_status(self, product: models.Product) -> str:
        if product.inventory < 10:
            return "Low"
        else:
            return "OK"

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "payment_status", "placed_at")
    list_per_page = 10
    list_select_related = ("customer",)


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "membership")
    list_editable = ("membership",)
    list_per_page = 10


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ("title", "product_count")
    list_per_page = 10

    @admin.display(ordering="products_count")
    def product_count(self, collection: models.Collection) -> int:
        url = (
            reverse("admin:store_product_changelist")
            + "?"
            + urlencode({
                "collection__id": str(collection.id),
            })
            )
        return format_html("<a href='{}'> {}</a>", url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count("product")
        )
