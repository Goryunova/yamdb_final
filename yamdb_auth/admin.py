from django.contrib import admin

from .models import CustomUser


class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'email')


admin.site.register(CustomUser, UsersAdmin)
