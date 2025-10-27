from rest_framework import serializers
from .models import DailyActivity

class DailyActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyActivity
        fields = ['id', 'user', 'title', 'description', 'date', 'created_at']
        read_only_fields = ['id', 'user', 'date', 'created_at']

