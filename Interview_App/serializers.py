from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import AudioFile , Questions

class AudioFileSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Questions.objects.all(), allow_null=True, required=False)

    class Meta:
        model = AudioFile
        fields = ['recording', 'question']

    def validate_question(self, value):
        return value