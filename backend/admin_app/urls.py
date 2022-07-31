from django.urls import path
from admin_app.views import (
    ProductAPIView
)

urlpatterns = [
    path("products", ProductAPIView.as_view(), name="product control by admin")
]
