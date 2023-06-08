from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class MemberManager(BaseUserManager):
    def create_member(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        member = self.model(email=email, **extra_fields)
        member.set_password(password)
        member.save()
        return member


class Member(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField('auth.Group', related_name='members', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='members', blank=True)

    objects = MemberManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        # Handle permissions here
        return True

    def has_module_perms(self, app_label):
        # Handle permissions here
        return True


class Car(models.Model):
    owner_name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    plate_number = models.CharField(max_length=20)
    color = models.CharField(max_length=20)
    model = models.CharField(max_length=50)

    def __str__(self):
        return self.plate_number
