from django.contrib import admin
from .models import Profile,Post,LikePost,FollowersList,Comment

#register your models here

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)



class FollowersListTable(admin.ModelAdmin):
    list_display = ('follower', 'following_user', 'followed_at')  # Display fields in admin list view
    search_fields = ('follower__username', 'following_user__username')  # Add search fields for better admin usability

    # Optionally, you can add filters based on your model fields
    list_filter = ('followed_at',)


admin.site.register(FollowersList,FollowersListTable)



admin.site.register(Comment)