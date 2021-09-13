from django.contrib.auth.models import User
from .models import Profile
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from django.core.mail import send_mail
from django.conf import settings

# @receiver(post_save, sender=Profile)

#=========================================================#
def createProfile(sender, instance, created, **kwargs):
    """signal for creating a profile for new added user"""
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            username = user.username,
            email = user.email,
            name =user.first_name,
        )
        #welcome email
        subject = "welcome to devsocial"
        body = "we are glad you join our family ..."
        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently = False,
        )

#=====================================================#
def updateUser(sender, instance, created,**kwargs):
    """signal for updating user info when profile info is updated"""
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()

#=============================================#
def deleteUser (sender, instance, **kwargs):
    """signal for delete user when profile is deleted"""
    user = instance.user
    user.delete()
    print("user deleted")

#==========connecting signal receiver and sender==========#
post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)