from unicodedata import category
from django.db import models

from authentication.models import User


class ExpensesModel(models.Model):
    CATEGORY_OPTION = [
        ('Online_service', 'Online_service' ),
        ('Travel','Travel'),
       ( 'Food', 'Food'),
        ('Rent','Rent'),
        ('Others', 'Others')

    ]
    option = models.CharField(max_length=300, choices=CATEGORY_OPTION)
    amount = models.DecimalField(max_digits=10, decimal_places=2, max_length=300)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False)


    def __str__(self):
        return f"{self.owner}'s income"
