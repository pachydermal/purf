import datetime
from django.utils import timezone
from django.db import models

#REMOVE BLANK=TRUES FOR NEEDED FIELDS plz

DEPTS = (
    ('ANT', 'Anthropology'),
    ('ARC', 'Architecture'),
    ('ART', 'Art & Archaeology'),
    ('AST', 'Astrophysical Sciences'),
    ('CBE', 'Chemical and Biological Engineering'),
    ('CHM', 'Chemistry'),
    ('CEE', 'Civil and Environmental Engineering'),
    ('CLA', 'Classics'),
    ('COM', 'Comparative Literature'),
    ('COS', 'Computer Science'),
    ('EAS', 'East Asian Studies'),
    ('EEB', 'Ecology and Evolutionary Biology'),
    ('ECO', 'Economics'),
    ('ELE', 'Electrical Engineering'),
    ('ENG', 'English'),
    ('FRE', 'French and Italian'),
    ('GEO', 'Geosciences'),
    ('GER', 'German'),
    ('HIS', 'History'),
    ('IND', 'Independent Concentration'),
    ('MAT', 'Mathematics'),
    ('MAE', 'Mechanical and Aerospace Engineering'),
    ('MOL', 'Molecular Biology'),
    ('MUS', 'Music'),
    ('NES', 'Near Eastern Studies'),
    ('ORF', 'Operations Research and Financial Engineering'),
    ('PHI', 'Philosophy'),
    ('PHY', 'Physics'),
    ('POL', 'Politics'),
    ('PSY', 'Psychology'),
    ('REL', 'Religion'),
    ('SLA', 'Slavic Languages and Literatures'),
    ('SOC', 'Sociology'),
    ('SPA', 'Spanish and Portuguese'),
    ('UND', 'Undecided'),
    ('WWS', 'Woodrow Wilson School'),
)

class Professor(models.Model):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200,blank=True)
    department = models.CharField(max_length=200, choices=DEPTS)
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
    max_capacity = models.PositiveIntegerField(blank=True,null=True,default=0)
    current_capacity = models.PositiveIntegerField(blank=True,null=True,default=0)
    #previous advisees
    #rating
    #pub_date = models.DateTimeField('date published')
    def __unicode__(self):
        return self.name
    def __title__(self):
        return self.title
    def __email__(self):
        return self.email

class Student(models.Model):
    professor = models.ForeignKey(Professor,blank=True,null=True, default=None)
    name = models.CharField(max_length=200)
    department = models.CharField(max_length=200, choices=DEPTS)
    year = models.PositiveIntegerField()
    #image
    email = models.EmailField()
    website_link = models.URLField(blank=True)
    resume_link = models.URLField(blank=True)
    description = models.TextField(blank=True)
    #prev prof
    #certs
    research_interests = models.TextField(blank=True)
    def __unicode__(self):  
        return self.name
        
