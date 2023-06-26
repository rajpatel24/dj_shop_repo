from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ProductListView, csv_to_db

router = DefaultRouter()

router.register(r'products', ProductListView, basename='product')

urlpatterns = router.urls

urlpatterns += [
    path(r'csv-to-db/', csv_to_db.as_view(), name='interview_recording')
]
