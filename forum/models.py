from django.db import models
from accounts.models import COUNTRIES, User
from autoslug import AutoSlugField
from django.db.models import Count
from datetime import datetime, timedelta
from math import log
from django.urls import reverse
# Create your models here.


class ThreadRanker(models.QuerySet):
    def rank(self, method, time):
        qs = self
        if time == 'month':
            qs = qs.filter(created_at__gte=datetime.now()-timedelta(days=31))
        elif time =='year':
            qs = qs.filter(created_at__gte=datetime.now()-timedelta(days=365))
        elif time == 'week':
            qs = qs.filter(created_at__gte=datetime.now()-timedelta(days=7))
        if method =='top':
            qs = qs.annotate(upvotes=Count('upvote')).order_by('-upvotes')
        elif method == 'hot':
            qs = qs.order_by('-hot_score')
        return qs #sort by new 

def upload_dest_forum(instance, filename):
    filebase, extension = filename.split('.')
    path = "thread/%Y/%m/%d/"
    path = path + str(instance.pk) + "." + extension
    return path

class Category(models.Model):
    name = models.CharField(max_length=100)

class Board(models.Model):
    moderators = models.ManyToManyField(User, blank=True, related_name='moderates')
    name = models.CharField(max_length=255)
    description = models.TextField()
    rules = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    country = models.CharField(max_length=3, choices=COUNTRIES, null=True, default=None, blank=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    slug = AutoSlugField(populate_from='name')

    def get_absolute_url(self):
        return reverse('view_board', kwargs={'board_slug': self.slug})

class Thread(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='threads')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')
    title = models.CharField(max_length=255)
    text = models.TextField()
    image = models.ImageField(blank=True, upload_to=upload_dest_forum)
    created_at = models.DateTimeField(auto_now_add=True, null=True) #not on form
    last_edited = models.DateTimeField(auto_now=True) #not on form
    slug = AutoSlugField(populate_from='title', unique_with='board')
    objects = ThreadRanker.as_manager() #not a field
    hot_score = models.BigIntegerField(default=0)
    class Meta:
        ordering=['-created_at']
        unique_together=['slug', 'board']
    def get_hot_score(self):
        votes = self.upvotes.count()
        order = log(votes, 10)
        time = self.created_at.timestamp() - 1609459200 #this is 1/1/2021 in unix time
        total_score = round(order + time / 72000, 7) #reddit uses /45000 which is about 12 hours (each 12 hours the value of upvotes decreases), we use 20 hours in anticipation of low posts initially 
        return total_score
    @property
    def upvotes(self):
        upvotes = Upvote.objects.filter(thread=self)
        return upvotes.count()
    def get_absolute_url(self):
        return reverse('view_thread', kwargs={'board_slug': self.board.slug, 'thread_slug': self.slug})


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='replies')
    text = models.TextField()

    @property
    def upvotes(self):
        upvotes = Upvote.objects.filter(comment=self)
        return upvotes.count()

class Upvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, null=True, blank=True, related_name='upvotes')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

