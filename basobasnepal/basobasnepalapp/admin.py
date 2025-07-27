from django.contrib import admin
from .models import Room, Province, District, Municipality

# Register your models here.

admin.site.register(Room)
admin.site.register(Province)
admin.site.register(District)
admin.site.register(Municipality)