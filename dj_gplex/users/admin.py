from django.contrib import admin
from .models import Profile, Relationship

class ProfileAdmin(admin.ModelAdmin):
    pass

class RelationshipAdmin(admin.ModelAdmin):
    pass


admin.site.register(Profile)
admin.site.register(Relationship)
