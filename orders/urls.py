from django.urls import path
from rest_framework.routers import DefaultRouter

from orders.views import OrdersViewset, WishlistViewset

router = DefaultRouter()

router.register(r'orders', OrdersViewset, basename='delivery_orders')
router.register(r'wishlist', WishlistViewset, basename='wishlist')
urlpatterns = router.urls
