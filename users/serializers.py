from rest_auth import serializers as auth_serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserDetailsSerializer(auth_serializers.UserDetailsSerializer):
    """
    Adds following extra attributes:
    mobile: Mobile Number of the user
    name: Name of the user. Replaces last_name & first_name
    """

    class Meta:
        model = User
        fields = ('pk', 'username', 'first_name', 'middle_name', 'last_name',
                  'email', 'mobile', 'joined_date', 'update_date', 'is_active', 'is_staff')
        read_only_fields = ('username', 'email')
