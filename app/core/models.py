"""
Database models for the application
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

class UserManager(BaseUserManager):
    """User manager class"""
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a new user"""
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password) # encrypt password
        user.save(using=self._db) # support multiple databases
        return user

    def create_superuser(self, email, password):
        """Create and save a new superuser"""
        user = self.create_user(email, password)
        user.is_superuser = True # is_superuser is created by PermissionsMixin
        user.is_staff = True # is_staff is created by PermissionsMixin
        user.save(using=self._db)
        return user
class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
