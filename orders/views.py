from django.shortcuts import render
from rest_framework import viewsets, status, authentication
from rest_framework.response import Response

from orders.models import Order, Whishlist
from orders.serializers import OrdersSerializer, WishlistSerializer


# Create your views here.


class OrdersViewset(viewsets.ModelViewSet):
    http_method_names = [u'get', u'post']
    serializer_class = OrdersSerializer
    authentication_classes = [
        authentication.TokenAuthentication
    ]
    permission_classes = [
        # permissions.IsAuthenticated,
        # IsDeliveryBoyOrCustomer
    ]

    def get_queryset(self):
        return Order.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                'message': 'Orders List',
                'success': True,
                'status': status.HTTP_200_OK,
                'data': serializer.data
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
                'message': 'Order Details',
                'success': True,
                'status': status.HTTP_200_OK,
                'data': serializer.data
            }
        )

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'user_id': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                'message': 'Order Created Successfully',
                'success': True,
                'status': status.HTTP_200_OK,
                'data': serializer.data
            }
        )


class WishlistViewset(viewsets.ModelViewSet):
    http_method_names = [u'get', u'post']
    serializer_class = WishlistSerializer
    authentication_classes = [
        authentication.TokenAuthentication
    ]
    permission_classes = [
        # permissions.IsAuthenticated,
        # IsDeliveryBoyOrCustomer
    ]

    def get_queryset(self):
        return Whishlist.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                'message': 'Wishlist List',
                'success': True,
                'status': status.HTTP_200_OK,
                'data': serializer.data
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
                'message': 'Wishlist Details',
                'success': True,
                'status': status.HTTP_200_OK,
                'data': serializer.data
            }
        )

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'user_id': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                'message': 'Wishlist Added Successfully',
                'success': True,
                'status': status.HTTP_200_OK,
                'data': serializer.data
            }
        )
