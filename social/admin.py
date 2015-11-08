from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .forms import SignupForm, UserUpdateForm
from .models import TemuUser


# Register your models here.
class TemuUserAdmin(UserAdmin):
    form = UserUpdateForm
    add_form = SignupForm

    list_display = ('username', 'is_superuser')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('is_superuser',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('username', 'password', 'password_confirm')
        })
    )
    search_fields = ('username',)
    ordering = ('username', 'join_date')
    filter_horizontal = ()


admin.site.register(TemuUser, TemuUserAdmin)
admin.site.unregister(Group)