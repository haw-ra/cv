# pyright: reportMissingModuleSource=false
from django.contrib import admin
from .models import Profile, Education, Experience, Skill

# تسجيل الجداول مع عرض حقل user
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'email', 'job_title']
    list_filter = ['user']

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(Skill)
