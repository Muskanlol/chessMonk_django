from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True, min_length = 8)

    class Meta:
        model = CustomUser
        fields =  ['full_name', 'age', 'gender', 'email', 'password', 'profile_pic']

    
    def create(self, validated_data):
        password = validated_data.pop('password')

        user = CustomUser(**validated_data)   #unpacks into key values from dict
        user.set_password(password)  #hashes the passsword
        user.username = validated_data['email'].split('@')[0]

        user.save()
        return user
    

# login part

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only = True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(username = email, password=password)

        if not user:
            raise serializers.ValidationError('Invalid email or password😰')
        
        if not user.is_active:
            raise serializers.ValidationError('This account has been deactivated😱')
        
        data['user'] = user
        return data

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'full_name', 'email', 'age', 'gender', 'profile_pic']

        
    


