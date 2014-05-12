# models.py: contains Django models Professor, Student, Rating, Project, Department

import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

YEARS = ( ('Freshman','Freshman'),('Sophomore','Sophomore'),('Junior','Junior'), ('Senior', 'Senior'),)
DEPTS = ( ('CHM','CHM'),('COS','COS'),('ELE','ELE'), ('MOL','MOL'),('Other', 'Other'),('Undecided', 'Undecided'),)

# All fields except for title and advisees filled through scraping. All professors set as "open" initially
class Professor(models.Model):
    netid = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    department = models.CharField(max_length=200,choices=DEPTS)
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

# email filled automatically using netid; fields such as resume_link, research_interests for future features
class Student(models.Model):
    netid = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    department = models.CharField(max_length=200,choices=DEPTS)
    email = models.EmailField()
    image = models.URLField(max_length=200,blank=True)
    website_link = models.URLField(blank=True)
    year = models.CharField(max_length=200,choices=YEARS)
    resume_link = models.URLField(blank=True)
    description = models.TextField(blank=True)
    previous_professors = models.ManyToManyField('Professor',blank=True,null=True,default=None, related_name='previous_professors')
    research_interests = models.TextField(blank=True)
    certificates = models.TextField(blank=True)
    favorited_professors = models.ManyToManyField('Professor',blank=True,null=True,default=None, related_name='favorited_professors')
    def __unicode__(self):  
        return self.name

# Initial ratings populated using survey results. RatingForm will be used for future population
class Rating(models.Model):
    professor = models.ForeignKey('Professor')
    responsive = models.PositiveIntegerField()
    frequency = models.PositiveIntegerField()
    idea_input = models.PositiveIntegerField()
    overall = models.PositiveIntegerField()
    comments = models.TextField(blank=True)

# Projects populated using spreadsheets from CHM, MOL, COS, and ELE.
class Project(models.Model):
    professor = models.ForeignKey('Professor')
    student_name = models.CharField(max_length=200, blank=True)
    netid = models.CharField(max_length=200, blank=True)
    project_title = models.CharField(max_length=500)
    project_description = models.TextField(blank=True)
    type_of_project = models.CharField(max_length=200)
    department = models.CharField(max_length=200,choices=DEPTS)
    link = models.URLField(blank=True) 

class Department(models.Model):
    name = models.CharField(max_length=200)
    research_areas = models.TextField(blank=True)
