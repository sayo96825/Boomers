from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Topic of the room
class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
# Room where user will post messages
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
       ordering = ['-updated', '-created']

    def __str__(self):
        return self.name

#User can post multiple messages in a room
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]
# This function is called whenever a new user is created.
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.add(instance.profile)
        user_profile.save()

#Each user has a profile
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name =models.CharField(max_length=200, null=True)
    follows = models.ManyToManyField("self", related_name="followed_by",symmetrical=False,blank=True)
    bio = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank =True, upload_to='images', default='default-profile-image.png')
    skill = models.CharField(max_length =100, null=True,blank=True)
    generation = models.CharField(max_length =50, null=True,blank=True)

    USERNAME_FIELD = 'user'
    REQUIRED_FIELDS = []
    def __str__(self):
        return str(self.user)

    
    