from rest_framework import serializers
from .models import HistoryQuestion, HistoryQuiz

class HistoryQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryQuiz
        fields = [
            'id',
            'number',
            'subject',
            'accuracy',
            ]
           
    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance


class HistoryQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryQuestion
        fields = [
            'question',
            'anw_a', 
            'anw_b', 
            'anw_c', 
            'anw_d', 
            'anw', 
            'anw_correct'
        ]