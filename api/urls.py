from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import routers
from api import views
from api.views import *

router=routers.DefaultRouter()
router.register(r'farms', FarmViewset, basename='farms' )
router.register(r'products', ProductViewset, basename='products')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('login/',CustomAuthToken.as_view()),
    path('logout/', LogoutView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('farmer/create', views.farmer_signup, name='FarmerSignup'),
    path('famer/<int:farm_id>/', FarmerUpdateView.as_view(), name='UpadteFarmer'),
    path('famer/<int:farm_id>/', FarmerDeleteView.as_view(), name='DeleteFarmer'),
    path('buyer/create', views.buyer_signup, name='BuyerSignup'),
    path('transporter/create', views.transporter_signup, name='TransporterSignup'),
    path('farms/', AddFarm.as_view(), name='NewFarm'),
    path('farms/<int:farm_id>/', GetFarm.as_view(), name='FarmDetail'),
    path('farms/<int:farm_id>/', UpdateFarm.as_view(), name='UpdateFarm' ),
    path('farms/<int:farm_id>/', DeleteFarm.as_view(), name='DeleteFarm'),
    path('products/', AddProduct.as_view(), name='NewProduct'),
    path('products/<int:product_id>/', UpdateProduct.as_view(), name='UpdateProduct'),
    path('products/<int:product_id>/', DeleteProduct.as_view(), name='DeleteProduct'),
    path('order/all', OrderList.as_view(), name='OrderList'),
    path('order/', AddOrder.as_view(), name='AddOrder'),
    path('order/<int:order_id>/', UpdateOrder.as_view(), name='UpdateOrder'),
    path('order/<int:order_id>/', DeleteOrder.as_view(), name='CancelOrder'),
    path('transportation/all', TransportationList.as_view(), name='TransportationList'),
    path('transportation/', AddTransportaion.as_view(), name='AddTransportation'),
    path('transportation/<int:transportation_id>/', DeleteTransportation.as_view(), name='DeleteTransportation'),
    path('transportation/<int:transportation_id>/', UpdateTransportation.as_view(), name='UpdateTransportation'),
]
