
from django.contrib import admin

from ads.models.models import User, PointRecord, ExchangeRecord, ExchangeProduct, Channel

class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'dev_id', 'total_points', 'is_enable')

class PointRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'channel', 'task', 'point')

class ExchangeRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'account', 'amount')

class ExchangeProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'price', 'score', 'info')

class ChannelAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'order', 'is_enable')

admin.site.register(User, UserAdmin)
admin.site.register(PointRecord, PointRecordAdmin)
admin.site.register(ExchangeRecord, ExchangeRecordAdmin)
admin.site.register(Channel, ChannelAdmin)
admin.site.register(ExchangeProduct, ExchangeProductAdmin)

