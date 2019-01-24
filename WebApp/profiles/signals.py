from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from allauth.account.signals import user_signed_up
from .models import Profile


@receiver(user_signed_up)
def user_signed_up(request, user, sociallogin = None, **kwargs):
    if hasattr(sociallogin, 'account') and sociallogin.account.provider == 'Google':
        # Retrieve the first name and the last name from the facebook account
        # Build the username by concatenating the two names, with dot [.] between them
        #in progress
        user.save()
        # prof.save()
        # Ensure username is unique
        # Save the new username on the user's account

@receiver(post_save, sender=User)
def profile_save(sender, instance, created, **kwargs):
    if created is True:
        # we would need to create the object
        prof = Profile(user=instance)
        prof.save()
    else:
        #we are updating the object
        print("Updating an object")