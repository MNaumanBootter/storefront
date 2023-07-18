from django.urls import path
from rest_framework_nested import routers
from store import views

router = routers.DefaultRouter()
router.register("products", views.ProductViewSet, basename="product")
router.register("collections", views.CollectionViewSet)
router.register("carts", views.CartViewSet)
router.register("customers", views.CustomerViewSet)
router.register("orders", views.OrderViewSet, basename="orders")


products_router = routers.NestedDefaultRouter(router, "products", lookup="product")
products_router.register("reviews", views.ReviewViewSet, basename="product-reviews")
products_router.register("images", views.ProductImageViewSet, basename="product-images")

cartitems_router = routers.NestedDefaultRouter(router, "carts", lookup="cart")
cartitems_router.register("items", views.CartItemViewSet, basename="cart-items")

urlpatterns = (
    router.urls
    + products_router.urls
    + cartitems_router.urls
    + [
        path('email', views.email_test),
    ]
)
