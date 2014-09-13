# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AgeGroup'
        db.create_table(u'masters_agegroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('age_group', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'masters', ['AgeGroup'])

        # Adding model 'Role'
        db.create_table(u'masters_role', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('level', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'masters', ['Role'])

        # Adding model 'SessionType'
        db.create_table(u'masters_sessiontype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session_type', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'masters', ['SessionType'])

        # Adding model 'Activities'
        db.create_table(u'masters_activities', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('activities', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'masters', ['Activities'])

        # Adding model 'Experience'
        db.create_table(u'masters_experience', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('experience', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
        ))
        db.send_create_signal(u'masters', ['Experience'])

        # Adding model 'JobType'
        db.create_table(u'masters_jobtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('job_type', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'masters', ['JobType'])

        # Adding model 'State'
        db.create_table(u'masters_state', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('country', self.gf('django_countries.fields.CountryField')(max_length=2)),
        ))
        db.send_create_signal(u'masters', ['State'])

        # Adding model 'City'
        db.create_table(u'masters_city', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['masters.State'])),
        ))
        db.send_create_signal(u'masters', ['City'])

        # Adding model 'Hobby'
        db.create_table(u'masters_hobby', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'masters', ['Hobby'])

        # Adding model 'Center'
        db.create_table(u'masters_center', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.IntegerField')()),
            ('established_since', self.gf('django.db.models.fields.DateField')()),
            ('center_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('address_1', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('address_2', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('address_3', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('landmark', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['masters.City'])),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=6)),
        ))
        db.send_create_signal(u'masters', ['Center'])

        # Adding model 'GlobalEvent'
        db.create_table(u'masters_globalevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'masters', ['GlobalEvent'])

        # Adding model 'LocalEvent'
        db.create_table(u'masters_localevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'masters', ['LocalEvent'])

        # Adding model 'GNCSewa'
        db.create_table(u'masters_gncsewa', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
        ))
        db.send_create_signal(u'masters', ['GNCSewa'])


    def backwards(self, orm):
        # Deleting model 'AgeGroup'
        db.delete_table(u'masters_agegroup')

        # Deleting model 'Role'
        db.delete_table(u'masters_role')

        # Deleting model 'SessionType'
        db.delete_table(u'masters_sessiontype')

        # Deleting model 'Activities'
        db.delete_table(u'masters_activities')

        # Deleting model 'Experience'
        db.delete_table(u'masters_experience')

        # Deleting model 'JobType'
        db.delete_table(u'masters_jobtype')

        # Deleting model 'State'
        db.delete_table(u'masters_state')

        # Deleting model 'City'
        db.delete_table(u'masters_city')

        # Deleting model 'Hobby'
        db.delete_table(u'masters_hobby')

        # Deleting model 'Center'
        db.delete_table(u'masters_center')

        # Deleting model 'GlobalEvent'
        db.delete_table(u'masters_globalevent')

        # Deleting model 'LocalEvent'
        db.delete_table(u'masters_localevent')

        # Deleting model 'GNCSewa'
        db.delete_table(u'masters_gncsewa')


    models = {
        u'masters.activities': {
            'Meta': {'object_name': 'Activities'},
            'activities': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'masters.agegroup': {
            'Meta': {'object_name': 'AgeGroup'},
            'age_group': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'masters.center': {
            'Meta': {'object_name': 'Center'},
            'address_1': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'address_2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'address_3': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.IntegerField', [], {}),
            'center_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['masters.City']"}),
            'established_since': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'landmark': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '6'})
        },
        u'masters.city': {
            'Meta': {'object_name': 'City'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['masters.State']"})
        },
        u'masters.experience': {
            'Meta': {'object_name': 'Experience'},
            'experience': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'masters.globalevent': {
            'Meta': {'object_name': 'GlobalEvent'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'masters.gncsewa': {
            'Meta': {'object_name': 'GNCSewa'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        },
        u'masters.hobby': {
            'Meta': {'object_name': 'Hobby'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'masters.jobtype': {
            'Meta': {'object_name': 'JobType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'masters.localevent': {
            'Meta': {'object_name': 'LocalEvent'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'masters.role': {
            'Meta': {'object_name': 'Role'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'masters.sessiontype': {
            'Meta': {'object_name': 'SessionType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'masters.state': {
            'Meta': {'object_name': 'State'},
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['masters']