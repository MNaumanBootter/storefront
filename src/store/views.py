from django.core.mail import send_mail, mail_admins, BadHeaderError, EmailMessage
from django.http import HttpResponse
from templated_mail.mail import BaseEmailMessage

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from store.permissions import IsAdminOrReadOnly, ViewCustomerHistoryPermission
from store.pagination import DefaultPagination
from store.models import (
    Order,
    Product,
    Collection,
    ProductImage,
    Review,
    Cart,
    OrderItem,
    CartItem,
    Customer,
)
from store.filters import ProductFilter
from store.serializers import (
    CreateOrderSerializer,
    OrderSerializer,
    ProductImageSerialzer,
    ProductSerializer,
    CollectionSerializer,
    ReviewSerializer,
    CartSerializer,
    CartItemSerializer,
    AddCartItemSerializer,
    UpdateCartItemSerializer,
    CustomerSerializer,
    UpdateOrderSerializer,
)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.prefetch_related("images").all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ["title", "description"]
    ordering_fields = ["unit_price", "last_update"]

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs["pk"]).count() > 0:
            return Response(
                {
                    "error": "Product cannot be deleted because it is asoociated with an order item"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs["pk"]).count() > 0:
            return Response(
                {
                    "error": "Collection cannot be deleted because it is asoociated with a product"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs["product_pk"]).all()

    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_pk"]}


class CartViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = Cart.objects.prefetch_related("items__product").all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer
        elif self.request.method == "PATCH":
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs["cart_pk"]).select_related(
            "product"
        )

    def get_serializer_context(self):
        return {"cart_id": self.kwargs["cart_pk"]}


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    @action(
        detail=True,
        methods=["GET", "PUT"],
        permission_classes=[ViewCustomerHistoryPermission],
    )
    def history(self, request, pk):
        return Response("ok")

    @action(detail=False, methods=["GET", "PUT"], permission_classes=[IsAuthenticated])
    def me(self, request):
        customer = Customer.objects.get(user_id=request.user.id)
        if request.method == "GET":
            serializer = CustomerSerializer(customer)

        elif request.method == "PUT":
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid()
            serializer.save()
        return Response(serializer.data)


class OrderViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(
            data=request.data,
            context={"user_id": self.request.user.id},
        )
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateOrderSerializer
        if self.request.method == "PATCH":
            return UpdateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()

        customer_id = Customer.objects.only("id").get(user_id=user.id)
        return Order.objects.filter(customer_id=customer_id)


class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerialzer

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs["product_pk"]).all()

    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_pk"]}


def email_test(request):
    try:
        send_mail(
            "subject",
            "message",
            "from@example.com",
            ["user@example.com"],
            html_message="sup",
        )
        mail_admins(
            "subject",
            "message",
            html_message="sup",
        )
        message = EmailMessage(
            "subject", "message", "from@example.com", ["john@example.com"]
        )
        message.attach_file("store/static/store/styles.css")
        message.send()
        template_message = BaseEmailMessage(
            template_name="emails/hello.html",
            context={"name": "Name"},
        )
        template_message.send(["john@example.com"])
    except BadHeaderError:
        HttpResponse("Bad Header Error")
    return HttpResponse("hello")
