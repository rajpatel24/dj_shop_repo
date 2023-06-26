from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.text import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone
from django_extensions.db.models import TimeStampedModel

from phonenumber_field.validators import to_python

from .managers import UserManager


def validate_mobile(value):
    mobile_no = to_python(value)
    if not mobile_no and not mobile_no.is_valid():
        raise ValidationError(
            _('%(value)s is not a valid mobile number'),
            params={'value': value},
        )


class User(AbstractBaseUser, PermissionsMixin):
    """
    Default user model in a Django project.
    """
    username = models.CharField(verbose_name=_('Username'), max_length=254, unique=True)
    first_name = models.CharField(verbose_name=_('First Name'), max_length=50)
    middle_name = models.CharField(verbose_name=_('Middle Name'), max_length=50, null=True, blank=True)
    last_name = models.CharField(verbose_name=_('Last Name'), max_length=50)
    email = models.EmailField(verbose_name=_('Email Address'), unique=True)
    mobile = models.CharField("Mobile Number", validators=[validate_mobile], max_length=14, null=True, blank=True)
    joined_date = models.DateTimeField(verbose_name=_('Joined Date'), default=timezone.now)
    update_date = models.DateTimeField(verbose_name=_('Modified Date'), auto_now=True)
    is_active = models.BooleanField(verbose_name=_('Activated'), default=True)
    is_staff = models.BooleanField(verbose_name=_('Staff Status'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'mobile']

    def __str__(self):
        return "%s %s | %s" % (self.first_name, self.last_name, self.mobile)

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = f"c{self.email}"
            # do something here
        super(User, self).save(*args, **kwargs)
