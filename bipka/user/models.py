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
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(max_length=200, blank=False, unique=True)  # почта
    username = models.CharField(max_length=150, blank=False)  # название организации
    phone_no = models.CharField(max_length=11, blank=False)  # Телефон
    head = models.CharField(max_length=100, blank=False)  # Руководитель
    ogrn = models.CharField(max_length=15, blank=False, unique=True)  # ОГРНИП/ОГРН
    inn = models.CharField(max_length=12, blank=False, unique=True)  # ИНН
    address_reg = models.CharField(max_length=150, blank=False)  # Адрес регистрации
    address_fact = models.CharField(max_length=150, blank=False)  # Фактический адрес
    date_reg = models.DateTimeField(auto_now_add=True)  # Дата регистрации
    is_rest = models.BooleanField(default=False) # Ресторан или благотворительная организация
    is_ind_pred = models.BooleanField(default=False) # ИП или юридическое лицо

    is_active = models.BooleanField(default=False) # прошел ли пользователь регистрацию через почту
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    # defining the manager for the CustomUser model
    objects = CustomUserManager()

    def __str__(self):
        return str(self.email)

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

'''
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
'''
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
