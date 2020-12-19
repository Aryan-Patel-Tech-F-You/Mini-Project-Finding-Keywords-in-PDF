from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Files(models.Model):
    File_Name = models.CharField(max_length=100, default="")
    File = models.FileField(upload_to="AllFiles/", default="")
    Key = models.CharField(max_length=100, default="")

    def __str__(self):
        return f"File is {self.File_Name} and key is {self.Key}"
