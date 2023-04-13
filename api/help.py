from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import FarmerSerializer

@api_view(['POST'])
def farmer_signup(request):
    serializer = FarmerSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data['password'])
        user.is_farmer = True
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import serializers
from .models import Farmer, CustomUser

class FarmerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'contact')

    def create(self, validated_data):
        farmer_data = validated_data.pop('farmer', None)
        user = CustomUser.objects.create(**validated_data)
        Farmer.objects.create(user=user, **farmer_data)
        return user
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2', 'is_farmer', 'is_transporter', 'is_buyer', 'contact']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Les mots de passe doivent correspondre.")
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = CustomUser(**validated_data)
        if password is not None:
            user.set_password(password)
        user.save()
        return user
