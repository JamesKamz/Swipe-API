from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model=Farm
        fields='__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Farm
        fields='__all__'

class FarmListSerializer(serializers.ModelSerializer):
    class Meta:
        model= Farm
        fields=['id', 'name', 'address', 'owner']

class ProductSerailizer(serializers.ModelSerializer):
    class Meta:
        model= Product
        fields='__all__'

class FarmDetailSerializer(serializers.ModelSerializer):
    products=serializers.SerializerMethodField
    class Meta:
        model=Farm
        fields=['id', 'name', 'address', 'owner', 'products', 'active']
    
    def get_products(self, instance):
        queryset=instance.products.filter(active=True)
        serializer=ProductSerailizer(queryset, many=True)
        return serializer.data

class TransportationSerializer(serializers.ModelSerializer):
    class Meta:
        model=t=Transportation
        fields='__all__'

class regSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        field = 'email'

class FarmerSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={"input_type":"password"}, write_only=True)
    
    class Meta:
        model = CustomUser
        fields =['username','first_name', 'last_name','email','contact','password', 'password2'] 
        extra_kwargs={
            'password':{'write_only':True}
        }
    
    def save(self, **kwargs):
        user=CustomUser(
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            email=self.validated_data['email'],
            contact=self.validated_data['contact']
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        if password !=password2:
            raise serializers.ValidationError({"error":"password do not match"})
        user.set_password(password)
        user.is_farmer=True
        user.save()
        Farmer.objects.create(user=user)
        return user

class TransporterSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={"input_type":"password"}, write_only=True)

    class Meta:
        model = CustomUser
        fields =['username','first_name', 'last_name','email','password', 'password2'] 
        extra_kwargs={
            'password':{'write_only':True}
        }
    
    def save(self, **kwargs):
        user=CustomUser(
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            email=self.validated_data['email'],
            contact=self.validated_data['contact']
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        if password !=password2:
            raise serializers.ValidationError({"error":"password do not match"})
        user.set_password(password)
        user.is_transporter=True
        user.save()
        Transporter.objects.create(user=user)
        return user
    

class BuyerSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={"input_type":"password"}, write_only=True)

    class Meta:
        model = CustomUser
        fields =['username','first_name', 'last_name','email','password', 'password2']
        extra_kwargs={
            'password':{'write_only':True}
        } 
    
    def save(self, **kwargs):
        user=CustomUser(
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            email=self.validated_data['email'],
            contact=self.validated_data['contact']
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        if password !=password2:
            raise serializers.ValidationError({"error":"password do not match"})
        user.set_password(password)
        user.is_buyer=True
        user.save()
        Buyer.objects.create(user=user)
        return user