from django.contrib import admin
from models import UserProfile, Friendship

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'studentid')
    
    list_filter = ('dorm', 'user__date_joined')
    
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'studentid')
    
    readonly_fields = ('activation_key',)

class FriendshipAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Friendship, FriendshipAdmin)