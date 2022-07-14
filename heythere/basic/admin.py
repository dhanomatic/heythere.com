from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class UserRegInline(admin.StackedInline):
    model = UserRegister
    can_delete: False
    verbose_name_plural: 'UserRegister'

class CustomizedUserAdmin (UserAdmin):
    inlines = (UserRegInline, )

admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)

admin.site.register(Neighbourhood)
admin.site.register(UserRegister)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Circle)