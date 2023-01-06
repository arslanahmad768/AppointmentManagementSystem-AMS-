from django.contrib.auth.models import AbstractUser
from django.db import models
# from .manager import UserManager
import datetime
import os

# Create your models here.

def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('uploads/', filename)

class User(AbstractUser):
    email = models.EmailField(verbose_name="Enter Email", unique=True,max_length=255)
    # username = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    # objects = UserManager()

# User._meta.get_field('first_name').validators[1].limit_value = 255

class ExcelFileUpload(models.Model):
    excel_file = models.FileField(upload_to="excel")

class Employe(models.Model):
    Status_choices = [
    ('Single', 'Single'),
    ('Married', 'Married'),
    ]

    Industry_choices = [
        ('Agriculture', 'Agriculture'),
        ('Construction', 'Construction'),
        ('Education', 'Education'),
        ('Energy Supply', 'Energy Supply'),
        ('IT', 'IT'),
    ]
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phoneno = models.CharField(max_length=15)
    age = models.IntegerField()
    status = models.CharField(max_length=15,choices=Status_choices)
    image = models.ImageField(upload_to=filepath, null=True, blank=True)
    industry = models.CharField(max_length=20,choices=Industry_choices)
    description = models.TextField(max_length=200)

    def __str__(self):
        return self.user.username
class Appointment(models.Model):
    calender = models.DateTimeField()
    employe = models.ForeignKey(Employe,on_delete=models.CASCADE)

    def __str__(self):
        return self.employe.user.username