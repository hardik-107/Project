from django.contrib import admin

from .models import User,Student

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_dispaly=('id','name','email','password')
    
@admin.register(Student)
class UserAdmin(admin.ModelAdmin):
    list_display=('id','name','email','age','grade')