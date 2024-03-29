from django.db import models
from accounts.models import User
from django.urls import reverse
from django.db.models import UniqueConstraint, Q
#from autoslug import AutoSlugField

REPO_ACCESS = (
    ('write', 'write'),
    ('read', 'read'),
    ('triage', 'triage'),
    ('maintain', 'maintain'),
    ('admin', 'admin')
)
 
METHOD = (
    ('Crpyotcurrency', (
        ('USDC', 'USD Coin'),
        ('BTC', 'Bitcoin'),
        ('ETH', 'Ethereum'),
        ('BCH', 'Bitcoin Cash')
        )
    )
)

class ProjectSearch(models.QuerySet):
    def search(self, string, license):
        return self #implement search logic 

class License(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(unique=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    ACCESS = (
        ('public', 'Public'),
        ('private', 'Private'),
        ('open', 'Open')
    )
    PERIOD = (
        ('monthly', 'Monthly'),
        ('weekly', 'Weekly'),
        ('na', 'N/A')
    )
    name = models.CharField(max_length=200, unique=True) #autogenerate from GitHub repo
    repo_name = models.CharField(max_length=100, unique=True)
    access_level = models.CharField(choices=ACCESS, max_length=10) #can community vote with unallocated vote? can community bring proposals? can community see project state? 
    description = models.TextField()
    _license = models.ForeignKey(License, on_delete=models.SET_NULL, null=True)
    founders = models.ManyToManyField(User)
    currency = models.CharField(max_length=10, choices=METHOD, default='BCH', blank=True)
    policies = models.TextField(default='') #code of conduct/commit policies/etc.
    quorum = models.PositiveSmallIntegerField() #in percentage
    minimum_number_of_votes_for = models.PositiveSmallIntegerField() #in percentage
    proposal_days_active = models.PositiveSmallIntegerField() #in days
    objects = ProjectSearch.as_manager() #not a field
    published = models.BooleanField(default=False)
    disbursemenets = models.CharField(choices=PERIOD, max_length=10)
    members = models.ManyToManyField(User, blank=True)

    @property
    def star_count(self):
        stars = Star.objects.filter(project=self)
        return stars.count()
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('view_project', kwargs={'project_name': self.name})

##POOL##
class AbstractPool(models.Model):
    name = models.CharField(max_length=200, unique=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='pools')
    revenue_share = models.PositiveSmallIntegerField()
    vote_share = models.PositiveSmallIntegerField()
    unallocated = models.BooleanField(default=False) 
    repo_access = models.CharField(max_length=10, choices=REPO_ACCESS)
    class Meta:
        abstract=True
    def __str__(self):
        return self.name

class Pool(AbstractPool):
    pass
######
##GROUP##
#class AbstractGroup(models.Model):
#    name = models.CharField(max_length=200)
#    description = models.TextField()
#    users = models.ManyToManyField(User)
#    def __str__(self):
#        return self.name
#    class Meta:
#        abstract=True
#
#class Group(AbstractGroup):
#    pass
##

##PRODUCT##
class AbstractProduct(models.Model):
    TYPE = (
        ('license', 'License'),
        ('paid', 'Premium Software'),
        ('enterprise', 'Enterprise Edition'),
        ('subscription', 'Subscription Service')
        ##expand this (read wikipedia page on business models)
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='products')
    name= models.CharField(max_length=200)
    description = models.TextField()
    _type = models.CharField(max_length=20, choices=TYPE)
    recurring = models.BooleanField(default=False)
    class Meta:
        abstract=True
    def __str__(self):
        return self.name

class Product(AbstractProduct):
    class Meta:
        unique_together=['name', 'project']

class AbstractPaymentPeriod(models.Model):
    PERIOD = (
        ('O', 'One Time'),
        ('W', 'Weekly'),
        ('M', 'Monthly'),
        ('Y', 'Yearly'),
    )
    price = models.PositiveSmallIntegerField()
    period = models.CharField(max_length=1, choices=PERIOD)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        abstract=True
    def __str__(self):
        string = self.product.project.currency + str(self.price) + " " + self.get_period_display()
        return string
class PaymentPeriod(AbstractPaymentPeriod):
    pass
#####

##ROLE##
class AbstractRole(models.Model):
    name = models.CharField(max_length=200)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    pool = models.ForeignKey(Pool, on_delete=models.PROTECT)
    users = models.ManyToManyField(User)
    #vacancies = models.PositiveSmallIntegerField(default=0)

    class Meta:
        abstract=True
    def __str__(self):
        return self.name

class Role(AbstractRole):
    pass

#####
##RELEASE##

def release_dir_path(instance, filename):
    #file will be uploaded to releases/<project_name>/<product_name>/<release_tag>
    extension = filename.split('.')[1]
    path = 'releases/' + instance.product.project.name + '/' + instance.product.name + '/' + instance.tag_name + extension
    return path

#following GitHub API specification
class AbstractRelease(models.Model):
    tag_name = models.CharField(max_length=100)
    release_name = models.CharField(max_length=20, default='')
    body = models.TextField(null=True)
    draft = models.BooleanField(default=False)
    prerelease = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    binary_compiled = models.FileField(upload_to=release_dir_path) #validate and upload
    
    class Meta:
        abstract=True

class Release(AbstractRelease):
    class Meta:
        unique_together = ['tag_name', 'product', 'prerelease']
#####

##GOAL##
class AbstractGoal(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    text= models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(default=None, null=True)
    number = models.PositiveSmallIntegerField() #number of goals 
    reward = models.PositiveSmallIntegerField(default=0)
    completed_by = models.ManyToManyField(User, blank=True)

    class Meta:
        abstract=True
    def __str__(self):
        string = self.project.__str__() + " " + str(self.number)
        return string

class Goal(AbstractGoal):
    pass
####
class Proposal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    description =  models.TextField(default='') 
    published = models.BooleanField(default=False) #auto
    active = models.BooleanField(default=False) #auto
    passed = models.BooleanField(default=False) #auto
    passed_date = models.DateTimeField(default=None, null=True) #auto
    created_at = models.DateTimeField(auto_now_add=True) #auto
    expiry_date = models.DateTimeField(default=None, null=True) #auto
    number = models.SmallIntegerField(default=-1) #number of proposal - auto

    def __str__(self):
        return self.project.__str__() + " " + str(self.number)
    def get_absolute_url(self):
        return reverse('view_proposal', kwargs={'project_name': self.project.repo_name, 'num': self.number})
    class Meta:
        unique_together=['number', 'project']
        constraints = [UniqueConstraint(fields=['user', 'project'], condition=Q(published=False), name='unique_unpublished_proposal')]

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ay = models.BooleanField()
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE) #motion?
    explanation = models.TextField()

    class Meta:
        unique_together=['user', 'proposal']

class Star(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='stars')
    project=models.ForeignKey(Project, on_delete=models.CASCADE, related_name='stars')

    class Meta:
        unique_together=['user', 'project']

####MOTIONS####

class Motion(models.Model): #to bundle together different proposals 
    justification = models.TextField(default='')
    proposal = models.ForeignKey(Proposal, related_name='motions', on_delete=models.CASCADE)
    delete = models.BooleanField(default=False)

class GoalMotion(Motion, AbstractGoal):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        pass

class ReleaseMotion(Motion, AbstractRelease): #new or update
    release = models.ForeignKey(Release, on_delete=models.CASCADE, null=True, default=None)

class RoleMotion(Motion, AbstractRole): #new or update
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, default=None) 

#class GroupMotion(Motion, AbstractGroup): #new or update
#    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, default=None)

class PoolMotion(Motion, AbstractPool): #new or update
    pool = models.ForeignKey(Pool, on_delete=models.CASCADE, null=True, default=None)


class ProjectMotion(Motion): #update
    _license = models.ForeignKey(License, on_delete=models.SET_NULL, null=True)
    currency = models.CharField(max_length=10, choices=METHOD)
    policies = models.TextField(default='') #code of conduct/commit policies/etc.
    quorum = models.PositiveSmallIntegerField() #in percentage
    proposal_days_active = models.PositiveSmallIntegerField() #in days

#product (one proceess)
class ProductMotion(Motion, AbstractProduct): #new or update
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, default=None)


class PaymentPeriodMotion(Motion, AbstractPaymentPeriod): #new or update
    pp = models.ForeignKey(PaymentPeriod, on_delete=models.CASCADE, null=True, default=None)
###

class HRMotion(Motion): #hire or fire
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL,null=True)


#MOTIONS LIST:
#admin:
#Project
#HR
#Role
#Release
#financial:
#Product + Payment Period
#Pool
#Goal