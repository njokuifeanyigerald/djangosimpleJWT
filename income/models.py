from unicodedata import category
from django.db import models

from authentication.models import User


class IncomeModel(models.Model):
    SOURCE_OF_INCOME = [
        ('SALARY', 'SALARY' ),
        ('BUSINESS','BUSINESS'),
       ( 'SIDE-HUSTLES', 'SIDE-HUSTLES'),
        ('OTHERS', 'OTHERS')

    ]
    source = models.CharField(max_length=300, choices=SOURCE_OF_INCOME)
    amount = models.DecimalField(max_digits=10, decimal_places=2, max_length=300)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False)
    
    # class Meta:
    #     ordering: ['-date']

    def __str__(self):
        return  f"{self.owner}'s income"
