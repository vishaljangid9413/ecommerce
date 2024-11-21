from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from cart.models import CartItem
from .manager import UserManager


def name_validation(value):
    if value and not all(char.isalpha() or char.isspace() for char in value):
        raise ValidationError("Name must contain only alphabetic characters.")    

def number_validation(value):
    if not value or len(str(value)) < 10:
        raise ValidationError("Mobile number must contain 10 digits")


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100, null=True, blank=True, validators=[name_validation])
    email = models.EmailField(unique=True)
    mobile = models.IntegerField(unique=True, validators=[number_validation])

    registration_datetime = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "mobile"
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email
    

    

