from django.contrib import admin
from models import UserProfile, Friendship

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'studentid')
    
    readonly_fields = ('activation_key',)

class FriendshipAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Friendship, FriendshipAdmin)