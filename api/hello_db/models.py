from django.db import models

# Create your models here.

class Hello(models.Model):
    world = models.CharField(max_length=255)

    class Meta:
        db_table = "hello"