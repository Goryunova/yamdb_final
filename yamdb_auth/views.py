import random
import secrets

import django.db.utils
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.settings import DEFAULT_FROM_EMAIL
from yamdb.models import User

from .models import ConfirmationCode


@api_view(['POST'])
@permission_classes([AllowAny])
def send_code(request):
    try:
        email = request.data['email']
    except KeyError:
        return Response({"error": 'Email required'},
                        status=status.HTTP_400_BAD_REQUEST)

    length = random.randint(13, 20)
    code = secrets.token_hex(length)

    ConfirmationCode.objects.filter(email=email).delete()
    ConfirmationCode.objects.create(email=email, confirmation_code=code)

    send_mail(
        'YaMDB Code',
        f'there is your code: {code}',
        f'{DEFAULT_FROM_EMAIL}',
        [email],
        fail_silently=False,
    )

    return Response({'email': email}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user_and_get_token(request):
    try:
        email = request.data['email']
        code = request.data['confirmation_code']
    except KeyError as ex:
        return Response({"error": f'field {ex} is required'},
                        status=status.HTTP_400_BAD_REQUEST)

    if ConfirmationCode.objects.filter(email=email, confirmation_code=code):
        username = email.split('@')[0]

        try:
            user = User.objects.create(username=username, email=email)
        except django.db.utils.IntegrityError:
            user = get_object_or_404(User, email=email)

        token = AccessToken.for_user(user=user)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)
