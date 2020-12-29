from django.db import models


class Project(models.Model):
    pass

class Role(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    
