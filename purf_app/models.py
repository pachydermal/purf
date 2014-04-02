import datetime
from django.utils import timezone
from django.db import models

#REMOVE BLANK=TRUES FOR NEEDED FIELDS plz

class Professor(models.Model):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200,blank=True)
	#department = models.CharField(max_length=200)
    #image = models.ImageField()
    email = models.EmailField()
    office = models.CharField(max_length=200,blank=True)
    phone = models.CharField(max_length=200,blank=True)
    WASS = models.URLField(max_length=200,blank=True)
    research_areas = models.TextField(blank=True)
    research_topics = models.TextField(blank=True)
    research_links = models.TextField(blank=True)
    website_link = models.URLField(blank=True)
    description = models.TextField(blank=True)
    max_capacity = models.PositiveIntegerField()
    current_capacity = models.PositiveIntegerField()
    #previous advisees
    #rating
    #pub_date = models.DateTimeField('date published')
    def __unicode__(self):
        return self.name
    def __title__(self):
        return self.title
    def __email__(self):
        return self.email
    #def was_published_recently(self):
    #    return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Student(models.Model):
    professor = models.ForeignKey(Professor)
    name = models.CharField(max_length=200)
    #dept
    year = models.PositiveIntegerField()
    #image
    email = models.EmailField()
    website_link = models.URLField()
    resume_link = models.URLField()
    description = models.TextField()
    #prev prof
    #certs
    research_interests = models.TextField()
    def __unicode__(self):  
        return self.name
        