from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Location)
admin.site.register(Hotel)
admin.site.register(Booking)
admin.site.register(Reviews)