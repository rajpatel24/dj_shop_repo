import csv
from decimal import Decimal

from django.shortcuts import render
from rest_framework import viewsets, status, authentication
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import Order
from .models import Product
from .serializers import ProductSerializer
from .utils import recommended_product_based_on_history


# Create your views here.


class ProductListView(viewsets.ModelViewSet):
    http_method_names = [u'get']
    serializer_class = ProductSerializer
    # authentication_classes = [
    #     authentication.TokenAuthentication
    # ]
    permission_classes = [
        # permissions.IsAuthenticated,
        # IsDeliveryBoyOrCustomer
    ]

    def get_queryset(self):
        return Product.objects.all()[200:500]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        if request.user.is_authenticated:
            print("\n\n ===>>>>", request.user)
            orders = Order.objects.filter(user=request.user)
            if not orders:
                rating_wise_recommended_products = Product.objects.order_by('-rating')[:5]
                recommended_products = self.get_serializer(rating_wise_recommended_products, many=True)
            else:
                recommended_data = recommended_product_based_on_history(last_purchase_id=orders.first().product.product_id)
                rating_wise_recommended_products = Product.objects.filter(product_id__in=recommended_data)
                recommended_products = self.get_serializer(rating_wise_recommended_products, many=True)
        else:
            rating_wise_recommended_products = Product.objects.order_by('-rating')[:5]
            recommended_products = self.get_serializer(rating_wise_recommended_products, many=True)

        # Add a static value 'Recommended' to each object in recommended_products
        recommended_products_data = recommended_products.data
        for product_data in recommended_products_data:
            product_data['status'] = 'Recommended'

        # Combine serializer.data and recommended_products_data
        combined_data = recommended_products_data + serializer.data

        return Response(
            {
                'message': 'Product List',
                'success': True,
                'status': status.HTTP_200_OK,
                'data': combined_data
            }
        )

    def retrieve(self, request, *args, **kwargs):
        """
        Get product details

        Only delivery boy and customer can access it

        **Example Response:**

            {
                "message": "Product Details",
                "success": true,
                "status": 200,
                "data": {
                    "id": 2,
                    "name": "Pomegranate",
                    "quantity": 4,
                    "our_price": "220.00",
                    "market_price": "280.00",
                    "description": "",
                    "quality": "A",
                    "is_active": true
                }
            }
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response(
            {
                'message': 'Product Details',
                'success': True,
                'status': status.HTTP_200_OK,
                'data': serializer.data
            }
        )


class csv_to_db(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    http_method_names = [u'get']

    def get(self, request):
        def clean_price(price_str):
            # # Remove currency symbol and comma characters
            # price_str = price_str.replace('₹', '').replace(',', '')
            # return Decimal(price_str)

            # Remove currency symbol and comma characters
            price_str = price_str.replace('₹', '').replace(',', '')

            try:
                return Decimal(price_str)
            except (ValueError, TypeError):
                # Handle invalid or missing values, return a default value or None if appropriate
                return None

        def clean_discount(discount_str):
            # Remove percentage symbol
            discount_str = discount_str.replace('%', '')
            return Decimal(discount_str)

        def clean_rating_count(rating_count):
            # Remove currency symbol and comma characters
            rating_count = rating_count.replace(',', '')
            return Decimal(rating_count)

        def import_data_from_csv():
            with open('/home/raj/Downloads/Dhruv-Surani/backend/dj_shop/amazon.csv', 'r') as csv_file:
                reader = csv.reader(csv_file)
                next(reader)  # Skip the header row if present

                for row in reader:
                    try:
                        # Assuming the CSV file has columns: name, price, description
                        product_id = row[0]
                        product_name = row[1]
                        category = row[2]
                        discounted_price = clean_price(row[3])
                        actual_price = clean_price(row[4])
                        discount_percentage = clean_discount(row[5])
                        rating = Decimal(row[6])
                        rating_count = clean_rating_count(row[7])
                        about_product = row[8]
                        user_id = row[9]
                        user_name = row[10]
                        review_id = row[11]
                        review_title = row[12]
                        review_content = row[13]
                        img_link = row[14]
                        product_link = row[15]

                        product = Product.objects.create(
                            product_id=product_id,
                            product_name=product_name,
                            category=category,
                            discounted_price=discounted_price,
                            actual_price=actual_price,
                            discount_percentage=discount_percentage,
                            rating=rating,
                            rating_count=rating_count,
                            about_product=about_product,
                            img_link=img_link,
                        )
                        product.save()
                    except Exception as e:
                        print(f"Error processing row: {row}")
                        print(f"Error message: {str(e)}")

        # Call the function and pass the path to your CSV file
        import_data_from_csv()

        return Response(
            {
                'message': 'successfully',
                'success': True,
                'status': status.HTTP_200_OK,
                'data': ""
            }
        )
