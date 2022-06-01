from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from user.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email inseted of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_admin(self):
        "Is the user a member of staff?"
        return self.is_staff
