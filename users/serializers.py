from rest_framework.serializers import ModelSerializer

from yamdb.models import User


class UsersSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role'
        ]
