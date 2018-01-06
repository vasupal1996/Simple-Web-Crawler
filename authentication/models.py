from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    contact = models.IntegerField(null=True, blank=True)
    profession = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    tagline = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        # db_table = ''
        # managed = True
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

@receiver(post_save, sender=User)
def CreateUserProfile(sender, instance, created,**kwargs):
    if created:
        Profile.objects.create(user=instance) 

@receiver(post_save, sender=User)
def SaveUserProfile(sender, instance,**kwargs):
    try:
        instance.profile.save()
    except:
        pass