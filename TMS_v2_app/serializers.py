from rest_framework import serializers
from .models import Tasks, Project, TaskAssignment, Comment

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = '__all__'

class TasksAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskAssignment
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class ProjectProgressSerializer(serializers.Serializer):
    project_id = serializers.IntegerField()
    progress_percentage = serializers.FloatField()