from django.db import models

# Create your models here.

class test(models.Model):
    test_title = models.CharField(max_length=100)
    test_desc = models.CharField(max_length=200)
    test_interp = models.CharField(max_length=300)
    price = models.IntegerField()

    def __str__(self):
        return self.test_title
