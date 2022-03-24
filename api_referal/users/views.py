from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
import time
import string
import random

from .serializers import UserSerializer, ForeignCodeSerializer, ShowUserSerializer
from .models import InputInviteCode


User = get_user_model()


def send_sms(to, from_phone, body):
    time.sleep(2)


def generate_code(size, char=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(char) for _ in range(size))


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


@api_view(['post'])
@permission_classes([AllowAny])
def registration_phone(request):
    phone_number = request.data.get('phone_number')
    invite_code = generate_code(size=6)
    serializer = UserSerializer(data=request.data, partial=True)
    confirmation_code = generate_code(size=4)
    serializer.is_valid(raise_exception=True)
    serializer.save(
        username=phone_number,
        confirmation_code=confirmation_code,
        invite_code=invite_code
    )
    send_sms(
        body=confirmation_code,
        from_phone=settings.SERVICE_PHONE,
        to=[phone_number]
    )
    return Response(
        f"Код который придет на телефон {confirmation_code}",
        status=status.HTTP_200_OK,
    )


@api_view(['post'])
@permission_classes([AllowAny])
def get_token(request):
    phone_number = request.data.get('phone_number')
    confirmation_code = request.data.get('confirmation_code')
    user = get_object_or_404(User, username=phone_number)
    if user.confirmation_code != confirmation_code:
        raise serializers.ValidationError('Неверно введен код потдверждения')
    token = get_tokens_for_user(user)
    user.is_active = True
    user.save()
    user_data = {
        'phone_number': phone_number,
        'confirmation_code': confirmation_code,
        'token': token
    }
    return Response(user_data, status=status.HTTP_201_CREATED)


@api_view(['get'])
@permission_classes([IsAuthenticated])
def me(request):
    user = get_object_or_404(User, pk=request.user.id)
    serializer = ShowUserSerializer(user, context=request)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['post'])
@permission_classes([IsAuthenticated])
def post_invite_code(request):
    user = request.user
    if InputInviteCode.objects.filter(my_code=user):
        return Response(
            'У вас уже есть активный инвайт код',
            status=status.HTTP_400_BAD_REQUEST
        )
    invite_code = request.data.get('invite_code')
    if user.invite_code == invite_code:
        return Response(
            'Вы не можете ввести свой инвайт код',
            status=status.HTTP_400_BAD_REQUEST
        )
    foreign_code = get_object_or_404(
        User,
        invite_code=invite_code
    )
    data = {
        "my_code": user.id,
        "foreign_code": foreign_code.id
    }
    serializer = ForeignCodeSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
