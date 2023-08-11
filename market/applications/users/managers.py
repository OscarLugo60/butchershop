from django.db import models
#
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager, models.Manager):

    def _create_user(self, user, password, is_staff, is_superuser, is_active, **extra_fields):
        user = self.model(
            user=user,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_user(self, user, password=None, **extra_fields):
        return self._create_user(user, password, False, False, True, **extra_fields)

    def create_superuser(self, user, password=None, **extra_fields):
        return self._create_user(user, password, True, True, True, **extra_fields)
    

    def usuarios_sistema(self):
        return self.filter(
            is_superuser=False
        ).order_by('-last_login')