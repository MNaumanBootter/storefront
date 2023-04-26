from django.contrib import admin
from store import models
from django.db.models import Count
from django.utils.html import format_html
from django.utils.http import urlencode
from django.urls import reverse

class InventoryFilter(admin.SimpleListFilter):
    title = "inventory"
    parameter_name = "inventory"

    def lookups(self, request, model_admin):
        return [
            ("<10", "Low")
        ]
    def queryset(self, request, queryset):
        if self.value() == "<10":
            return queryset.filter(inventory__lt=10)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "unit_price", "inventory_status", "collection_title")
    list_editable = ("unit_price",)
    list_filter = ("collection", "last_update", InventoryFilter)
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
    list_display = ("first_name", "last_name", "membership", "orders_count")
    list_editable = ("membership",)
    list_per_page = 10
    search_fields = ("first_name__istartswith", "last_name__istartswith")

    @admin.display(ordering="orders_count")
    def orders_count(self, customer: models.Customer) -> int:
        url = (
            reverse("admin:store_order_changelist")
            + "?"
            + urlencode({
                "customer__id": str(customer.id),
            })
            )
        return format_html("<a href='{}'> {}</a>", url, customer.orders_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count("order")
        )


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
