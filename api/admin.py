from django.contrib import admin
from .models import *

admin.site.register(CustomUser)
admin.site.register(Farmer)
admin.site.register(Transporter)
admin.site.register(Buyer)
admin.site.register(Farm)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Transportation)