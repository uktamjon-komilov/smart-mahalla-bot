from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.utils.html import format_html
import admin_thumbnails

from core.models import *


class ProfileAdmin(admin.ModelAdmin):
    list_display = ["tg_id", "tg_username", "first_name", "last_name"]


class MFYAdmin(admin.ModelAdmin):
    list_filter = ["city"]
    search_fields = ["city__title", "title"]
    

@admin_thumbnails.thumbnail("image")
class HelperInfographicAdmin(admin.ModelAdmin):
    list_display = ["get_image"]

    def get_image(self, obj=None):
        try:
            return format_html("<img src='{}' style='display: block; width: 300px; height: 300px;'/>".format(obj.image.url))
        except:
            return format_html("<div></div>")
    
    get_image.short_description = "Rasm"


@admin_thumbnails.thumbnail("image")
class LeaderInfographicAdmin(admin.ModelAdmin):
    list_display = ["get_image"]

    def get_image(self, obj=None):
        try:
            return format_html("<img src='{}' style='display: block; width: 300px; height: 300px;'/>".format(obj.image.url))
        except:
            return format_html("<div></div>")
    
    get_image.short_description = "Rasm"


admin.site.register(Profile, ProfileAdmin)
admin.site.register(City)
admin.site.register(Region)
admin.site.register(TelegramChannel)
admin.site.register(MFY, MFYAdmin)
admin.site.register(HelperInfographic, HelperInfographicAdmin)
admin.site.register(LeaderInfographic, LeaderInfographicAdmin)

admin.site.unregister(Group)
admin.site.unregister(User)