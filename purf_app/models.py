import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class Professor(models.Model):
    netid = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    email = models.EmailField()
    image = models.URLField(max_length=200,blank=True)
    website_link = models.URLField(blank=True)
    title = models.CharField(max_length=200,blank=True)
    office = models.CharField(max_length=200,blank=True)
    phone = models.CharField(max_length=200,blank=True)
    research_areas = models.TextField(blank=True)
    research_topics = models.TextField(blank=True)
    research_links = models.TextField(blank=True)
    description = models.TextField(blank=True)
    full = models.BooleanField(default=False)
    advisees = models.ManyToManyField('Student',blank=True,null=True,default=None)
    def __unicode__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    email = models.EmailField()
    image = models.URLField(max_length=200,blank=True)
    website_link = models.URLField(blank=True)
    year = models.PositiveIntegerField()
    resume_link = models.URLField(blank=True)
    description = models.TextField(blank=True)
    previous_professors = models.ManyToManyField('Professor',blank=True,null=True,default=None, related_name='previous_professors')
    research_interests = models.TextField(blank=True)
    certificates = models.TextField(blank=True)
    favorited_professors = models.ManyToManyField('Professor',blank=True,null=True,default=None, related_name='favorited_professors')
    def __unicode__(self):  
        return self.name

"""class User(models.Model):
    student = models.ForeignKey('Student',blank=True,null=True,default=None,related_name='controlled_student')
    professor = models.ForeignKey('Professor',blank=True,null=True,default=None,related_name='controlled_professor')
    preferences = models.TextField(blank=True)
    #favorited_students = models.ManyToManyField('Student',blank=True,null=True,default=None)
    #favorited_professors = models.ManyToManyField('Professor',blank=True,null=True,default=None)
    first_access = models.DateTimeField('Time of first access')
"""
class Rating(models.Model):
    professor = models.ForeignKey('Professor')
    responsive = models.PositiveIntegerField()
    frequency = models.PositiveIntegerField()
    idea_input = models.PositiveIntegerField()
    overall = models.PositiveIntegerField()
    comments = models.TextField(blank=True)

class Project(models.Model):
    professor = models.ForeignKey('Professor')
    student_name = models.CharField(max_length=200)
    student_email = models.CharField(max_length=200, blank=True)
    year = models.PositiveIntegerField()
    project_title = models.CharField(max_length=500)
    project_description = models.TextField(blank=True)
    type_of_project = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    link = models.URLField(blank=True) 
