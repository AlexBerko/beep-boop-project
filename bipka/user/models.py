from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from datetime import date
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import *

#################################################
#                                               #
#                   USER MODEL                  #
#                                               #
#################################################

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email or len(email) <= 0:
            raise ValueError("Email field is required!")
        if not password:
            raise ValueError("Password is must!")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(max_length=200, unique=True)
    # user = models.OneToOneField(AbstractBaseUser, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, blank=False, null=True, default='def')  # название организации
    phone_no = models.CharField(max_length=10, blank=False, default='def')
    form = models.CharField(max_length=32, blank=False, default='def')  # Форма организации
    head = models.CharField(max_length=100, blank=False, default='def')  # Руководитель
    ogrn = models.CharField(max_length=15, blank=False, default='def')  # ОГРНИП/ОГРН unique=True,
    inn = models.CharField(max_length=12, blank=False, default='def')  # ИНН unique=True,
    kpp = models.CharField(max_length=9, blank=False, default='def')  # КПП unique=True,
    address_reg = models.CharField(max_length=150, blank=False, default='def')  # Адрес регистрации
    address_fact = models.CharField(max_length=150, blank=False, default='def')  # Фактический адрес
    # date_reg = models.DateField(blank=False)  # Дата регистрации

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # special permission which define that
    # the new user is Restaurant or student
    is_rest = models.BooleanField(default=False)
    is_blago = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    # defining the manager for the CustomUser model
    objects = CustomUserManager()

    def __str__(self):
        return str(self.email)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class FundManager(models.Manager):
    def create_user(self, email, password=None):
        if not email or len(email) <= 0:
            raise ValueError("Email field is required !")
        if not password:
            raise ValueError("Password is must !")
        email = email.lower()
        user = self.model(
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return queryset


class Fund(CustomUser):
    class Meta:
        proxy = True

    objects = FundManager()

    def save(self, *args, **kwargs):
        self.is_blago = True
        return super().save(*args, **kwargs)


class RestaurantManager(models.Manager):
    def create_user(self, email, password=None):
        if not email or len(email) <= 0:
            raise ValueError("Email field is required !")
        if not password:
            raise ValueError("Password is must !")
        email = email.lower()
        user = self.model(
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return queryset


class Restaurant(CustomUser):
    class Meta:
        proxy = True

    objects = RestaurantManager()

    def save(self, *args, **kwargs):
        self.is_rest = True
        return super().save(*args, **kwargs)

#################################################
#                                               #
#                   OTP  MODEL                  #
#                                               #
#################################################

class OtpModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=7)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.otp

#################################################
#                                               #
#                   HELP MODEL                  #
#                                               #
#################################################

class Help(models.Model):
    # id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255, blank=False, default='def')
    full_info = models.TextField(blank=False, default='def')
    org_info = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    pubdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

