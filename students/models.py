from django.db import models
from django.utils import timezone
from class_app.models import Classes
# Create your models here.

class Student(models.Model):
    student_id = models.CharField(max_length=1000,blank=True)
    name =  models.CharField(max_length=1200,blank=True)
    Class_id =  models.ForeignKey(Classes,on_delete=models.CASCADE)    
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)