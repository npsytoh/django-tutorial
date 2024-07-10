from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Profile
from .forms import CustomAdminChangeForm


class UserAdmin(BaseUserAdmin):
    form = CustomAdminChangeForm

    list_display = (
        'email',
        'active',
        'staff',
        'admin',
    )
    list_filter = (
        'admin',
        'active',
    )
    ordering = ('email',)
    filter_horizontal = ()
    search_fields = ('email',)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2')
        }),
    )

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('プロフィール', {'fields': (
            'username',
            'department',
            'phone_number',
            'gender',
            'birthday',
        )}),
        ('Permissions', {'fields': ('staff','admin',)}),
    )

admin.site.register(User, UserAdmin)