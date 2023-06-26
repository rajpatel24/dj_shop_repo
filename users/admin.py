from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from django.utils.text import gettext_lazy as _

from .models import User


class DRFUserAdmin(UserAdmin):
    """
    Overrides UserAdmin
    """
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'middle_name', 'last_name', 'email', 'mobile')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff',
                                       'is_superuser',
                                       )}),
        (_('Important dates'), {'fields': ('last_login', 'joined_date',
                                           'update_date')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name',
                       'email', 'mobile', 'groups',
                       'password1', 'password2'),
        }),
    )

    list_display = ('username', 'first_name', 'last_name', 'email', 'mobile', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'mobile', )
    readonly_fields = ('joined_date', 'last_login', 'update_date')
    list_filter = ('is_active', 'is_staff')


class StaffAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'user', 'is_active')


admin.site.register(User, DRFUserAdmin)