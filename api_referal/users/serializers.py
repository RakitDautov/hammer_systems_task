from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import ForeignCode
from rest_framework.validators import UniqueTogetherValidator


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class WithMyCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone_number', )


class ShowUserSerializer(serializers.ModelSerializer):
    users_with_my_invite = serializers.SerializerMethodField("get_users")
    input_invite_code = serializers.SerializerMethodField("get_input_invite_code")

    class Meta:
        model = User
        fields = (
            'phone_number',
            'invite_code',
            'users_with_my_invite',
            'input_invite_code'
        )

    def get_users(self, obj):
        foreign_users = ForeignCode.objects.filter(foreign_code=obj)
        foreign_code_phone = []
        for users in foreign_users:
            foreign_code_phone.append(users.user.phone_number)
        return foreign_code_phone

    def get_input_invite_code(self, obj):
        return ForeignCode.objects.get(user=obj).foreign_code.invite_code


class ForeignCodeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    foreign_code = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    class Meta:
        model = ForeignCode
        fields = ("user", "foreign_code")
        validators = [
            UniqueTogetherValidator(
                queryset=ForeignCode.objects.all(),
                fields=["user", "foreign_code"],
            )
        ]
