from django.contrib import admin
from Modules.MenuOrdersApp.models import *

# Register your models here.
admin.site.register(Menus)
admin.site.register(Meals)
admin.site.register(Orders)
admin.site.register(Permissions)
admin.site.register(Users)
admin.site.register(UsersPermissions)
