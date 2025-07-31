from django.contrib import admin
from .models import Province, District, Municipality, Room
from django.utils.html import format_html

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('id',)

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'province')
    list_filter = ('province',)
    search_fields = ('name',)
    ordering = ('id',)

@admin.register(Municipality)
class MunicipalityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'district')
    list_filter = ('district',)
    search_fields = ('name',)
    ordering = ('id',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'colored_approve', 'province', 'district', 'municipality', 'ward_num', 'num_of_rooms_available', 'contact_number')
    list_filter = ('province', 'district', 'municipality')
    search_fields = ('owner__username', 'description', 'street')
    raw_id_fields = ('owner',)
    ordering = ('approve',)

    def colored_approve(self, obj):
        if obj.approve:
            return format_html('<span style="color: green; font-weight: bold;">Approved</span>')
        else:
            return format_html('<span style="color: red; font-weight: bold;">Unapproved</span>')
    colored_approve.short_description = 'Approval Status'
