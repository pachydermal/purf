# Full path and name to your csv file
csv_filepathname="profs.tsv"
csv_filepathname2 ="Projects.tsv"
csv_filepathname3 ="Reviews.tsv"

# Full path to your django project directory
#your_djangoproject_home="/Users/Pallavi/COS_Archive/Classes/COS333/Project/"
your_djangoproject_home="C:/Users/Stephen/Documents/GitHub/purf/"
import sys, os
sys.path.append(your_djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from purf_app.models import Professor, Project, Rating

import csv
profdataReader = csv.reader(open(csv_filepathname), dialect='excel-tab')
projdataReader = csv.reader(open(csv_filepathname2), dialect='excel-tab')
ratdataReader = csv.reader(open(csv_filepathname3), dialect='excel-tab')

for i,row in enumerate(profdataReader):
    prof = Professor()
    prof.netid = row[0]
    prof.title = row[2]
    prof.office = row[6]
    prof.phone = row[7]
    prof.research_areas = row[9]
    prof.research_topics = row[10]
    prof.research_links = row[11]
    prof.description = row[13]
    prof.full = row[14]

    prof.name = row[1]
    prof.department = row[3]

    prof.email = row[5]
    prof.image = row[4]
    prof.website_link = row[12]

    prof.save()

for i,row in enumerate(projdataReader):
    proj = Project()
    try:
        proj.professor=Professor.objects.get(pk=row[1])
    except:
        continue

    proj.netid = row[3]
    proj.student_name=row[2]
    proj.year = row[4]
    proj.project_title=row[5]
    proj.project_description = row[6]
    proj.type_of_project=row[7]
    proj.department=row[8]

    proj.save()

for i,row in enumerate(ratdataReader):
    rat = Rating()
    try:
        rat.professor=Professor.objects.get(pk=row[0])
    except:
        continue

    rat.responsive = row[1]
    rat.frequency = row[2]
    rat.idea_input = row[3]
    rat.overall = row[4]
    rat.comments = row[5]

    rat.save()


