from rest_framework import serializers
from .models import User
from .dashboard import Dashboard

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name','first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password':{'write_only': True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class DashboardSerializer(serializers.Serializer):
    finished_quizes = serializers.IntegerField()
    subject_active = serializers.IntegerField()
    subject_created = serializers.IntegerField()
    quizes_generated = serializers.IntegerField()

    name = serializers.StringRelatedField()
    email = serializers.StringRelatedField()
    user_name = serializers.StringRelatedField()

