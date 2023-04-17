from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, UserProfile


# Signal creates UserProfile for every User
@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    # check if User is created correctly:

    if created:
        UserProfile.objects.create(user=instance)
    # if profile already exists - just save it
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            # if User already exists without profile - create UserProfile
            UserProfile.objects.create(user=instance)
