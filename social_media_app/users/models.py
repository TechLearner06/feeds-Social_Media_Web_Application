from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
import uuid


#create your models here

class Profile(models.Model):

    GENDER_CHOICES = [
        ('female', 'Female'),
        ('male', 'Male'),
        ('other', 'Other'),
    ]
    
    user = models.OneToOneField(get_user_model(), on_delete = models.CASCADE)
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    profile_img = models.ImageField(upload_to='profile_images' , default='user_dp.jpg')
    gender=models.CharField(max_length=6, choices=GENDER_CHOICES, default='other')
    
    
    
    

    def __str__(self):
        return self.user.username
    

class Post(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    image=models.ImageField(upload_to="posts/")
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    caption=models.TextField()
    created_at=models.DateTimeField(default=datetime.now)
    no_of_likes=models.IntegerField(default=0)
    location=models.CharField(blank=True,max_length=200)


    def __str__(self):
        return self.user.username
    

class LikePost(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username
    



class FollowersList(models.Model):
    follower = models.ForeignKey(get_user_model(), related_name='following', on_delete=models.CASCADE)  # the user following someone
    following_user = models.ForeignKey(get_user_model(), related_name='followers', on_delete=models.CASCADE)  # the user who is being followed
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following_user')  # this ensures that a user cannot follow the same user more than once


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.content[:20]}'
