# from random import choices

from os import read

from django.contrib.auth import get_user_model
from rest_framework import serializers

# from llc import user
# from user import User

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True, min_length=8)
    role = serializers.ChoiceField(choices=["student","instructor"], write_only = True)

    class Meta:
        model = User
        fields = ["username","email","password","role"]

    def create(self,validated_data):
        role = validated_data.pop("role")
        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)

        if role == "is_instructor":
            user.is_instructor = True
            user.is_student = False
        else:
            user.is_instructor = False
            user.is_student = True

        user.save()
        return user
    
class MeSerializer(serializers.ModelSerializer):
    avater_url = serializers.CharField(read_only = True)

    class meta:
        model = User
        fields = ["id", "username", "email", "is_instructor", "is_student", "avater_url", "profile_image"]
        read_only_fields = ["id", "is_instructor", "is_student", "avater_url"]

