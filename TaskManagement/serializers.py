from rest_framework import serializers
from .models import Task

# we can use read-only serializers for reading for better performance
class TaskSerializer(serializers.ModelSerializer):
    days_until_due = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = '__all__'
        # read_only_fields = []

    def get_days_until_due(self, obj):
        from datetime import date
        delta = obj.due_date - date.today()
        return delta.days
    
    def to_representation(self, instance):
        # we can override response data here, if needed
        # self.Meta.model.objects.prefetch_related(Prefetch('related_model'))
        return super().to_representation(instance)

    '''

    def validate_title(self, value):
        if 'urgent' in value.lower() and self.initial_data.get('priority') != 'high':
            raise serializers.ValidationError("Urgent tasks must have high priority.")
        return value
    '''

    def create(self, validated_data):
        instance = super().create(validated_data)
        # Additional logic can go here
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        # Additional logic can go here
        return instance