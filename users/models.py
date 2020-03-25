import uuid

from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import ugettext_lazy as _

class UserManager(BaseUserManager):
    """ A user manager for the user model with email as username"""
    use_in_migrations = True


    def _create_user(self, email, password,**extra_fields):
        if not email:
            raise ValueError(_('Email address must be provided'))
        if not password:
            raise ValueError(_('Password must be provided'))
        email = self.normalize_email(email)
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff',False)
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(email,password,**extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_satff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self._create_user(email, password, **extra_fields)
   
class ShopUser(AbstractUser):
    """ Custom user model to accept email as username"""
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'


    username = None
    email = models.EmailField(_('email address'),unique=True, blank=False, null=False)
    is_active = models.BooleanField('active', default=True)
    is_verified = models.BooleanField('verified', default=False)  # Add the `is_verified` flag
    verification_uuid = models.UUIDField('Unique Verification UUID', default=uuid.uuid4)


    objects = UserManager()

    def __str__(self):
        return self.email


class SupplierUser(models.Model):
    user=models.ForeignKey(ShopUser,on_delete=models.CASCADE)
    name=models.CharField(max_length=255,null=False,blank=False)
    phonenumber=PhoneNumberField(null=False)
    address=models.TextField(max_length=500)
    def __str__(self):
        return self.name


class CustomerProfile(models.Model):
    user = models.OneToOneField(ShopUser, on_delete=models.CASCADE,related_name='customerProfile')
    birthdate = models.DateField(null=True,blank=True)



class Adress(models.Model):

    user = models.ForeignKey(ShopUser, on_delete=models.CASCADE)
    ostan_choices=(
        ('teh','تهران'),
        ('shiraz','شیراز'),
        ('esfahan','اصفهان'),
        ('tabriz','تبریز')
    )

    ostan=models.CharField(max_length=255,choices=ostan_choices,null=False)
    adress_detail=models.TextField(max_length=500,null=False,blank=False)
    pelak=models.CharField(max_length=100,null=False,blank=False)
    postal_code=models.CharField(max_length=100,null=False,blank=False)
    phone_number=PhoneNumberField()
    home_phone_number=PhoneNumberField()

