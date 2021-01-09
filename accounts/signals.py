from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User
from allauth.socialaccount.models import SocialAccount

@receiver(post_save, sender=User)
def generate_username(sender, instance, *args, **kwargs):
    if instance.username == None:
        try:
            username = SocialAccount.objects.get(user=instance).extra_data['login']
            instance.username = username
            instance.save()
        except:
            pass
