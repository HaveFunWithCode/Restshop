from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from .models import ShopUser, Adress

admin.site.register(Adress)


@admin.register(ShopUser)
class ShopUserAdmin(UserAdmin):
    """ Define Shop admin model for ShopUser model with no email field """

    fieldsets = (
        (None,{'fields':('email', 'password')}),
        (_('Personal info'),{'fields':('first_name','last_name')}),
        (_('Confirmation info'), {'fields': ('is_verified',)}),
        (_('Permissions'),{'fields':('is_active','is_staff','is_superuser','groups','user_permissions')}),
        (_('Important dates'),{'fields':('last_login','date_joined')}),

    )
    add_fieldsets =(
        (None,{
            'classes':('wide',),
            'fields':('email','password1','password2'),
        }),
    )
    # list_display = ('email', 'last_login', 'date_joined')
    # search_fields = ('email', 'last_login')
    # ordering = ('-last_login',)
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)