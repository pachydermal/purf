# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Professor.department'
        db.delete_column(u'purf_app_professor', 'department')


    def backwards(self, orm):
        # Adding field 'Professor.department'
        db.add_column(u'purf_app_professor', 'department',
                      self.gf('django.db.models.fields.CharField')(default='COS', max_length=200),
                      keep_default=False)


    models = {
        u'purf_app.professor': {
            'Meta': {'object_name': 'Professor'},
            'WASS': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'current_capacity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_capacity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'office': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'research_areas': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'research_links': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'research_topics': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'website_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'purf_app.student': {
            'Meta': {'object_name': 'Student'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'professor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['purf_app.Professor']"}),
            'research_interests': ('django.db.models.fields.TextField', [], {}),
            'resume_link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'website_link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['purf_app']