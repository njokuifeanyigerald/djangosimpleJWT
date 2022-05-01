from rest_framework import serializers
from .models import IncomeModel

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeModel
        fields = [
             'id', 'amount' ,'source', 'description','date'
        ]

