# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Professor'
        db.create_table(u'purf_app_professor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('department', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('office', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('WASS', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('research_areas', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('research_topics', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('research_links', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('website_link', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('max_capacity', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True, blank=True)),
            ('current_capacity', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True, blank=True)),
        ))
        db.send_create_signal(u'purf_app', ['Professor'])

        # Adding model 'Student'
        db.create_table(u'purf_app_student', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('professor', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['purf_app.Professor'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('department', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('year', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('website_link', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('resume_link', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('research_interests', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'purf_app', ['Student'])


    def backwards(self, orm):
        # Deleting model 'Professor'
        db.delete_table(u'purf_app_professor')

        # Deleting model 'Student'
        db.delete_table(u'purf_app_student')


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