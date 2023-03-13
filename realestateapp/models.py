from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser)
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **kwargs):

        if password is None:
            raise TypeError('Password should not be none')

        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        if password is None:
            raise TypeError('Password should not be none')

        if not email:
            raise ValueError('User must have an email address')

        kwargs.update({'is_superuser': True,
                       'is_staff': True,
                       'is_admin': True})

        user = self.model(
            email=self.normalize_email(email),
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    class LivingTypes(models.TextChoices):
        pass

    class IdentityTypes(models.TextChoices):
        HE = 'HE', 'He'
        SHE = 'SHE', 'She'
        THEY = 'THEY', 'They'

    email = models.EmailField(_('email address'), unique=True)

    # living_style = models.CharField(max_length=60, choices=LivingTypes.choices, blank=True, null=True)
    # necessity = models.CharField(max_length=60, choices=LivingTypes.choices, blank=True, null=True)
    # repairs_and_maintenance = models.CharField(max_length=60, choices=LivingTypes.choices, blank=True, null=True)
    # essentials = models.CharField(max_length=60, choices=LivingTypes.choices, blank=True, null=True)
    # decorate = models.CharField(max_length=60, choices=LivingTypes.choices, blank=True, null=True)
    # identity = models.CharField(max_length=60, choices=LivingTypes.choices, blank=True, null=True)

    # required fields
    date_joined = models.DateTimeField(auto_now_add=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# What is your preferred living style
# What must be something you have to have in your living space
# How do you want repairs and maintenance to be handled
# What essentials do you look for in a home
# What do you identify as e.g he/she/they

# How do you like to decorate your living space


class Apartment(models.Model):
    # id = models.BigIntegerField(primary_key=True, unique=True)
    price = models.FloatField(null=True, blank=True)
    min_price = models.FloatField(null=True, blank=True)
    max_price = models.FloatField(null=True, blank=True)
    cats = models.BooleanField(default=False, blank=True, null=True)
    dogs = models.BooleanField(default=False, blank=True, null=True)
    pet_policy_text = models.TextField(blank=True, null=True)
    beds = models.IntegerField(null=True, blank=True)
    min_beds = models.FloatField(null=True, blank=True)
    max_beds = models.FloatField(null=True, blank=True)
    baths = models.IntegerField(null=True, blank=True)
    min_baths = models.FloatField(null=True, blank=True)
    max_baths = models.FloatField(null=True, blank=True)
    house_type = models.CharField(max_length=100, null=True, blank=True)
    # sqft = models.IntegerField(null=True, blank=True)
    year_built = models.IntegerField(null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    postal_code = models.IntegerField(null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    permalink = models.CharField(max_length=100, null=True, blank=True)
    pictures = models.URLField()
    pictures1 = models.URLField()
    county = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.id} - {self.address}'
