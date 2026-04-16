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
        fields = ["first_name","last_name","username","email","password","role"]

    def create(self,validated_data):
        role = validated_data.pop("role")
        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)

        if role == "instructor":
            user.is_instructor = True
            user.is_student = False
        else:
            user.is_instructor = False
            user.is_student = True

        user.save()
        return user

class MeSerializer(serializers.ModelSerializer):
    # profile_image_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_instructor",
            "is_student",
            # "profile_image_url",
        ]

    # def get_profile_image_url(self, obj):
    #     request = self.context.get("request")
    #     if not obj.profile_image:
    #         return None
    #     if request is None:
    #         return obj.profile_image.url
    #     return request.build_absolute_uri(obj.profile_image.url)


# class ProfileImageUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ["profile_image"]



