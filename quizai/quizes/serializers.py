from rest_framework import serializers
from .models import Subject, Resoults 

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = [
            'id',
            'name',
            'level',
            'difficulty',
            'number_finished',
            'number_of_questions',
            'question',
            'level_class',
            ]

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance


class ResoultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resoults
        fields = [
            'id',
            'accuracy',
            'questions_quantity',
            'creation_date',
            'subject',
        ]

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
    