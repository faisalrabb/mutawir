from django.db import models
from accounts.models import User


class License(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

class Project(models.Model):
    name = #autogenerate from GitHub repo 
    currency = #enum
    _license = models.ForeignKey(License, on_delete=models.SET_NULL, null=True)


class Goal(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    text= models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(default=None, null=True)

class Role(models.Model):
    user = models.ForeignKey(User, on_delte=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
 

class Proposal(models.Model):
    user = models.ForeignKey(User, on_delte=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    votes_for = models.IntegerField(default=0)
    votes_against = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    passed = models.BooleanField(default=False)
    passed_date = models.DateTimeField(default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Financial(Proposal):
    pass
class Voting(Proposal):
    pass

class Transaction(Proposal):
    pass

class RoleUpdate(Proposal):
    pass

class ProjectUpdate(Proposal):
    pass

class GoalComplete(Proposal):
    pass

class Star(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='stars')
    project=models.ForeignKey(Project, on_delete=models.CASCADE, related_name='stars')

    
