from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.core.mail import send_mail
from dateutil.relativedelta import relativedelta
from datetime import date

# Create your models here.
USER_GOAL_CHOICES = (
    ('DOC', 'DOCTOR'),
    ('PAT', 'PATIENT')
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class USER(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    # first_name = models.CharField(max_length=30, null=False, blank=False)
    # last_name = models.CharField(max_length=30, null=False, blank=False)
    # user_goal = models.CharField(choices=USER_GOAL_CHOICES, max_length=7)
    # phone = models.CharField(max_length=15, unique=True, null=False, blank=False)
    # age = models.IntegerField(null=True, blank=True)
    # location = models.CharField(max_length=50, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics', default='profile_pics/default_profile.png')

    is_doctor = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


# SIGNALS
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
