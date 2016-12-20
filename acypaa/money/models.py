from __future__ import unicode_literals
from django.core.validators import validate_comma_separated_integer_list
from django.db import models

# Create your models here.

class Actual(models.Model):
    date = models.DateTimeField()
    category = models.IntegerField()
    amount = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    description = models.TextField()
    tags = models.CharField(default=0, max_length=200, validators=[validate_comma_separated_integer_list])

class Projected(models.Model):
    date = models.DateTimeField()
    category = models.IntegerField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    tags = models.CharField(max_length=200, validators=[validate_comma_separated_integer_list])
