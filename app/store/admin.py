from django.contrib import admin
from store import models

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "unit_price", "inventory_status", "collection_title")
    list_editable = ("unit_price",)
    list_per_page = 10
    list_select_related = ("collection",)

    @admin.display(ordering="inventory")
    def collection_title(self, product: models.Product) -> str:
        return product.collection.title

    @admin.display(ordering="inventory")
    def inventory_status(self, product: models.Product) -> str:
        if product.inventory < 10:
            return "Low"
        else:
            return "OK"

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "membership")
    list_editable = ("membership",)
    list_per_page = 10

admin.site.register(models.Collection)
