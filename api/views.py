from django.http import Http404
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, DestroyAPIView, RetrieveAPIView, UpdateAPIView, GenericAPIView
from rest_framework.response import Response
from .permissions import IsBuyerUser, IsFarmerUser, IsTransporterUser
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.response import Response


class FarmerUpdateView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, pk):
        try:
            farmer = Farmer.objects.get(pk=pk)
            self.check_object_permissions(self.request, farmer)
            return farmer
        except Farmer.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        farmer = self.get_object(pk)
        serializer = FarmerSerializer(farmer)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        farmer = self.get_object(pk)
        serializer = FarmerSerializer(farmer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FarmerDeleteView(APIView):
    def get_object(self, pk):
        try:
            farmer = Farmer.objects.get(pk=pk)
            self.check_object_permissions(self.request, farmer)
            return farmer
        except Farmer.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        farmer = self.get_object(pk)
        serializer = FarmerSerializer(farmer)
        return Response(serializer.data)
    def delete(self, request, pk, format=None):
        farmer = self.get_object(pk)
        farmer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FarmViewset (viewsets.ReadOnlyModelViewSet):
    serializer_class=FarmListSerializer
    detail_serializer=FarmDetailSerializer

    def get_queryset(self):
        return Farm.objects.filter(active=True)
    
    def get_serializer_class(self):
        if self.action=='retrive':
            return self.detail_serializer
        return super().get_serializer_class()

class ProductViewset (viewsets.ReadOnlyModelViewSet):
    serializer_class=ProductSerailizer

    def get_queryset(self):
        queryset=Product.objects.filter(active=True)
        farm_id=self.request.GET.get('farm_id')
        if farm_id is not None:
            queryset=queryset.get(farm_id=farm_id)
        return queryset

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

@api_view(['POST'])
def transporter_signup(request):
    serializer = TransporterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data['password'])
        user.is_transporter = True
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def buyer_signup(request):
    serializer = BuyerSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data['password'])
        user.is_buyer = True
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomAuthToken(GenericAPIView): # Login for both admin and customer accounts
    serializer_class=FarmerSerializer
    def post(self, request, *args, **kwargs):
        serializer=self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        token, created=Token.objects.get_or_create(user=user)
        return Response({
            'token':token.key,
            'user_id':user.pk,
            'is_farmer':user.is_farmer
        })

class LogoutView(APIView):
    def post(self, request, format=None):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)

#Create Farm
class AddFarm(CreateAPIView):
    serializer_class = FarmSerializer
    permission_classes=[permissions.IsAuthenticated and IsFarmerUser]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save() # user=request.user.farmer,
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Update Farm
class UpdateFarm(APIView):
    def get_object(self, pk):
        try:
            return Farm.objects.get(pk=pk)
        except Farm.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        farm = self.get_object(pk)
        serializer = FarmSerializer(farm, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete Farm
class DeleteFarm(APIView):
    permission_classes=[permissions.IsAuthenticated and IsFarmerUser]
    def get_object(self, pk):
        try:
            return Farm.objects.get(pk=pk)
        except Farm.DoesNotExist:
            raise Http404
            
    def delete(self, request, pk, format=None):
        farm= self.get_object(pk)
        farm.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Fetch single Farm information
class GetFarm(APIView):
    def get_object(self, pk):
        try:
            return Farm.objects.get(pk=pk)
        except Farm.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        farm = self.get_object(pk)
        products = Product.objects.filter(farm=farm.id).all()
        serializer = FarmSerializer(farm) #, RoomSerializer(rooms)
        # serializer = RoomSerializer(rooms)
        return Response(serializer.data)
    
#create product    
class AddProduct(CreateAPIView):
    serializer_class = ProductSerailizer
    permission_classes=[permissions.IsAuthenticated and IsFarmerUser]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save() # user=request.user.farmer,
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#update product
class UpdateProduct(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        product= self.get_object(pk)
        serializer = ProductSerailizer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Delete Product
class DeleteProduct(APIView):
    permission_classes=[permissions.IsAuthenticated and IsFarmerUser]
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404
            
    def delete(self, request, pk, format=None):
        product= self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#add an order     
class AddOrder(CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes=[permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save() # user=request.user.farmer,
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#update order
class UpdateOrder(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        order= self.get_object(pk)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Cancel or Delete order     
class DeleteOrder(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise Http404
            
    def delete(self, request, pk, format=None):
        order= self.get_object(pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#all order
class OrderList (APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get(self, request, format=None):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


#Add transportation
class AddTransportaion(CreateAPIView):
    serializer_class=TransportationSerializer
    permission_classes=[permissions.IsAuthenticated]
    def post(self, request):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

#List Transportation
class TransportationList (APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get(self, request, format=None):
        transportations=Transportation.objects.all()
        serializer=Transportation(transportations, many=True)
        return Response(serializer.data)

#update Transportation
class UpdateTransportation(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get_object(self, pk):
        try:
            return Transportation.objects.get(pk=pk)
        except Transportation.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        transport= self.get_object(pk)
        serializer = TransportationSerializer(transport, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Cancel or Delete transportation     
class DeleteTransportation(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get_object(self, pk):
        try:
            return Transportation.objects.get(pk=pk)
        except Transportation.DoesNotExist:
            raise Http404
            
    def delete(self, request, pk, format=None):
        order= self.get_object(pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
