from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import Roles, Users, Permissions, PermissionsRoles


class PermissionsRolesInline(admin.TabularInline):
    model = PermissionsRoles
    extra = 1


class RolesAdmin(admin.ModelAdmin):
    inlines = (PermissionsRolesInline,)
    list_display = ('pk', 'Name', 'Description')
    fieldsets = (
        ('Roles', {
            'fields': ('Name', 'Description', 'Active', 'Deleted')
        }),
    )
    
    
class UsersAdmin(UserAdmin):
    model = Users
    fieldsets = UserAdmin.fieldsets 
    #fieldsets[0][1]['fields'] = fieldsets[0][1]['fields'] + ('Roles',)
admin.site.register(Roles, RolesAdmin)
admin.site.register(Users, UsersAdmin)
admin.site.register(Permissions)