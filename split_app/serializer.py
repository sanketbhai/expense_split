from rest_framework import serializers
from .models import *

class OwnSerializer(serializers.ModelSerializer):
    simplified_amount = serializers.SerializerMethodField()
    Debtor_username = serializers.StringRelatedField(source='Debtor.username', read_only=True)
    Creditor_username = serializers.StringRelatedField(source='Creditor.username', read_only=True)

    class Meta:
        model = Own
        fields = ('id', 'Debtor', 'Creditor','Debtor_username','Creditor_username', 'amount','simplified_amount')
        read_only_fields = ('id', )

    def get_simplified_amount(self, obj):
        # Check if the user has simplified set to True
        user = obj.Creditor

        if user.simplify:
            return obj.simplified_amount
        else:
            return None  # or any other default value

