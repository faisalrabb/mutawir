from django.db import models
from django.contrib.auth.models import AbstractUser
#from django.contrib.postgres.fields import ArrayField
#from projects.models import Project, Role
from django.db.models import Q


# Create your models here.
#Country choices
COUNTRIES = (
    ('DZ','Algeria'),
    ('BH','Bahrain'),
    ('EG', 'Egypt'),
    ('IQ','Iraq'),
    ('JO', 'Jordan'),
    ('KW','Kuwait'),
    ('LB','Lebanon'),
    ('LY','Libya'),
    ('MR','Mauritania'),
    ('MA', 'Morocco'),
    ('OM','Oman'),
    ('PS', 'Palestine'),
    ('SY', 'Syria'),
    ('QA','Qatar'),
    ('KSA', 'Saudi Arabia'),
    ('SD','Sudan'),
    ('TN','Tunisia'),
    ('UAE','United Arab Emirates'),
    ('WS','Western Sahara'),
    ('YE','Yemen'),
    )

class UserQuerySet(models.QuerySet):
    def search(self, **kwargs):
        qs = self
        if kwargs.get('country',''):
            qs = qs.filter(country=kwargs['country'])
        if kwargs.get('skills', []):
            for skill in kwargs['skills']:
                qs = qs.filter(skills=skill)
        if kwargs.get('name', ''):
            qs = qs.filter(Q(fullname__contains=kwargs['name']) | Q(username__contains=kwargs['name']))
        return qs

class Skill(models.Model):
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text

def upload_dest(instance, filename):
    filebase, extension = filename.split('.')
    return 'pfp/%s.%s' % (str(instance.pk), extension)


class User(AbstractUser):
    username = models.CharField(max_length=39, default=None, null=True, unique=True) #not on form
    full_name = models.CharField(max_length=101, default='') #not on form
    crypto_balance = models.IntegerField(default=0) #not on form, DO NOT USE IN TEMPLATES
    paypal_balance = models.IntegerField(default=0) #not on form, DO NOT USE IN TEMPLATES
    profile_picture = models.ImageField(upload_to=upload_dest, default='pfp/default.png', blank=True)
    bio = models.TextField()
    linked_in_link = models.URLField(default=None, null=True, blank=True)
    country = models.CharField(max_length=3, choices=COUNTRIES)
    crypto_public_key = models.CharField(max_length=42, null=True, default=None, blank=True)
    paypal_email = models.EmailField(null=True, default=None, blank=True)
    skills= models.ManyToManyField(Skill, related_name='qualified', blank=True)
    objects = UserQuerySet.as_manager() #not a field
    search_ordering=models.IntegerField(default=0) #do not use, only for sorting search results by level of activity

    def get_absolute_url(self):
        return f"/accounts/<self.username>/"
    class Meta:
        ordering = ['-search_ordering']








