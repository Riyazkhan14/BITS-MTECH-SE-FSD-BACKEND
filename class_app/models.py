from django.db import models
from django.utils import timezone

# Create your models here.

class Classes(models.Model):
    name =  models.CharField(max_length=100,blank=True)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)