from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Institution(models.Model):
    institution_types = (
        ('C', 'fundacja'),
        ('NGO', 'organizacja pozarządowa'),
        ('L', 'zbiórka lokalna'),
    )
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField()
    type = models.CharField(max_length=128, choices=institution_types, default='C')
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return f'"{self.name}" ({self.type}, <{", ".join([cat.name for cat in self.categories.all()])}>)'


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=256)
    phone_number = models.CharField(max_length=32)
    city = models.CharField(max_length=128)
    zip_code = models.CharField(max_length=16)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)
    is_taken = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} => {self.institution.name}, {str(self.pick_up_date) + " " + str(self.pick_up_time)}'
