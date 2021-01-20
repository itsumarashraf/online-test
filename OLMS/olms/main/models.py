from django.db import models

# Create your models here.

class Messages(models.Model):
    name = models.CharField(max_length=50)
    email= models.CharField(max_length=50)
    message = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.name