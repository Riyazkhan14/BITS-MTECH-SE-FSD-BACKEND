from django.db import models
from django.contrib.auth.models import AbstractUser

from django.utils import timezone
# Create your models here.

#user Model
class CustomUser(AbstractUser):
    '''Overrides the custom django user model'''
    # Datafields
    SUPER_ADMIN = 1
    ADMIN = 2
    BUYERS = 3
    SELLERS = 4
    ROLE_CHOICES = (
      (SUPER_ADMIN,'Super Admin'),
      (ADMIN,'Admin')
    )
    name = models.CharField(max_length=100,blank=True)
    user_role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES,default=ADMIN)
    mobile_no = models.CharField(max_length=100)
    Updated_on = models.DateTimeField(default=timezone.now)
