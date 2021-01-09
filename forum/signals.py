from django.db.models.signals import post_save
from django.dispatch import receiver
from forum.models import Upvote

@receiver(post_save, sender=Upvote)
def update_hot_score(sender, instance, *args, **kwargs):
    if instance.thread is not None:
        score = instance.thread.get_hot_score()
        instance.thread.hot_score = score
        instance.thread.save()
