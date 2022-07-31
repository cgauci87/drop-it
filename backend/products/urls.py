from django.urls import path
from products.views import (
    ProductAPIView,
    ProductDetailAPIView,
    ProductReviewAPIView
)

urlpatterns = [
    path("", ProductAPIView.as_view(), name="product api"),
    path("product-detail", ProductDetailAPIView.as_view(), name="product-review"),
    path("user-review", ProductReviewAPIView.as_view(), name="user-review"),
]
