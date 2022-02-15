from django.contrib import admin
from django.contrib.auth.models import Group, User
from core.models import MFY, City, Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ["tg_id", "tg_username", "first_name", "last_name"]


class MFYAdmin(admin.ModelAdmin):
    list_filter = ["city"]
    


admin.site.register(Profile, ProfileAdmin)
admin.site.register(City)
admin.site.register(MFY, MFYAdmin)

admin.site.unregister(Group)
admin.site.unregister(User)