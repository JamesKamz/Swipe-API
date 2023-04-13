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
    path('buyer/create', views.buyer_signup, name='BuyerSignup'),
    path('transporter/create', views.transporter_signup, name='TransporterSignup'),
    path('farms/create', AddFarm.as_view(), name='NewFarm'),
    path('farms/read', ReadFarm.as_view(), name='FarmDetail'),
    path('farms/update', UdpdateFarm.as_view(), name='UpdateFarm' ),
    path('products/create', AddProduct.as_view(), name='NewProduct'),
]
