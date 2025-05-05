from django.db import models
from django.utils import timezone
from class_app.models import Classes
from students.models import Student
# Create your models here.

class Vaccine_Drives(models.Model):
    vaccine_name =  models.CharField(max_length=1200,blank=True)
    Class_id =  models.ForeignKey(Classes,on_delete=models.CASCADE)
    drive_date = models.DateField()
    available_slots = models.IntegerField()
    is_delete = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)

class Students_Vaccination(models.Model):
    Vaccine_id = models.ForeignKey(Vaccine_Drives,on_delete=models.CASCADE) 
    Student_id = models.ForeignKey(Student,on_delete=models.CASCADE) 
    vaccination_date = models.DateField(blank=True,null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)
