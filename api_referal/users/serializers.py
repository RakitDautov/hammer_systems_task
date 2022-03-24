from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import InputInviteCode


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class WithMyCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("phone_number",)


class ShowUserSerializer(serializers.ModelSerializer):
    users_with_my_invite = serializers.SerializerMethodField("get_users")
    input_invite_code = serializers.SerializerMethodField(
        "get_input_invite_code")

    class Meta:
        model = User
        fields = (
            "phone_number",
            "invite_code",
            "users_with_my_invite",
            "input_invite_code",
        )

    def get_users(self, obj):
        foreign_users = InputInviteCode.objects.filter(foreign_code=obj)
        foreign_code_phone = []
        for t in foreign_users:
            foreign_code_phone.append(t.my_code.phone_number)
        return foreign_code_phone

    def get_input_invite_code(self, obj):
        user = InputInviteCode.objects.filter(my_code=obj)
        input_code = ""
        for i in user:
            input_code += i.foreign_code.invite_code
        return input_code


class ForeignCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InputInviteCode
        fields = ("my_code", "foreign_code")
