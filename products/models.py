from django.db import models

# Create your models here.


class Product(models.Model):
    product_id = models.CharField(max_length=40, null=True, blank=True)
    product_name = models.CharField(max_length=40, null=True, blank=True)
    category = models.CharField(max_length=40, null=True, blank=True)
    discounted_price = models.DecimalField(max_digits = 7, decimal_places = 2, null=True, blank=True)
    actual_price = models.DecimalField(max_digits = 7, decimal_places = 2, null=True, blank=True)
    discount_percentage = models.DecimalField(max_digits = 7, decimal_places = 2, null=True, blank=True)
    rating = models.DecimalField(max_digits = 5, decimal_places = 2)
    rating_count = models.IntegerField(max_length=10, null=True, blank=True)
    about_product = models.CharField(max_length=500, null=True, blank=True)
    img_link = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
