from rest_framework import serializers
from django.core.exceptions import ValidationError

from .models import Task
# from account.models import User

class TaskCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(allow_blank=True, required=False)
    complete = serializers.BooleanField()
    class Meta:
        model = Task
        fields = ['user', 'title', 'description', 'complete']

    def create(self, attrs):
        
        print("This is from task create serializer", attrs)
        return Task.objects.create(**attrs)
    
    def update(self, instance, attrs):
        print(f" hey baby {instance}")
        instance.title = attrs.get('title', instance.title)
        instance.description = attrs.get('description', instance.description)
        instance.complete = attrs.get('complete', instance.complete)
        instance.save()

        return instance

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'complete']
