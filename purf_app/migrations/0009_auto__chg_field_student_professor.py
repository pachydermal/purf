# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Student.professor'
        db.alter_column(u'purf_app_student', 'professor_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['purf_app.Professor'], null=True))

    def backwards(self, orm):

        # Changing field 'Student.professor'
        db.alter_column(u'purf_app_student', 'professor_id', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['purf_app.Professor']))

    models = {
        u'purf_app.professor': {
            'Meta': {'object_name': 'Professor'},
            'WASS': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'current_capacity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'department': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
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
            'department': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'professor': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['purf_app.Professor']", 'null': 'True', 'blank': 'True'}),
            'research_interests': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'resume_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'website_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['purf_app']