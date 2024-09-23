from rest_framework import serializers
from players.models import Player
from rest_framework import serializers
from user.models import CustomUser
from django.contrib.auth import get_user_model

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'      


class NormalizedChoiceField(serializers.ChoiceField):
    def to_internal_value(self, data):
        # Normalize the input to lowercase
        data = data.lower()
        return super().to_internal_value(data)

class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(choices=[('coach', 'Coach'), ('agent', 'Agent')], required=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password', 'username', 'role']

    def create(self, validated_data):
        role = validated_data.pop('role')  # Extract the role of the user
        user = CustomUser(**validated_data)  
        user.set_password(validated_data['password'])  # Hash the password
        user.role = role  # Assign the role to the user
        user.save()  # Save the user
        return user

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
