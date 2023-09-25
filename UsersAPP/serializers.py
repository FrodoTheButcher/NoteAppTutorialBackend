
from rest_framework import serializers
from .models import  User
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username","email","password","id"]
    def create(self, validated_data):

        password = validated_data['password']
        passwordhashed = make_password(password)
        validated_data['password']=passwordhashed
        return super().create(validated_data)
    

class UserSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username","email"]
    def create(self, validated_data):

        password = validated_data['password']
        passwordhashed = make_password(password)
        validated_data['password']=passwordhashed
        return super().create(validated_data)
    