from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User
from allauth.socialaccount.models import SocialAccount
from allauth.account.signals import user_signed_up

#@receiver(post_save, sender=User)
#def generate_username(sender, instance, *args, **kwargs):
#    if instance.username == None:
#        try:
#            username = SocialAccount.objects.get(user=instance).extra_data['login']
#            instance.username = username
#            instance.save()
#        except:
#            pass

@receiver(user_signed_up)
def fill_username(sociallogin, user, **kwargs):
    user_data = user.socialaccount_set.filter(provider='github')[0].extra_data
    username = user_data['login']
    user.username = username
    user.save()
