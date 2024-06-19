from django.db import models
from django.contrib.auth.models import User


INSTITUTION_CHOICES = [
    (0, 'fundacja'),
    (1, 'organizacja pozarządowa'),
    (2, 'zbiórka lokalna'),
]


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Institution(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    type = models.CharField(choices=INSTITUTION_CHOICES, default=0)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)
