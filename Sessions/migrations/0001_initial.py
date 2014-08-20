# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'NewSession'
        db.create_table(u'Sessions_newsession', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('age_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['masters.AgeGroup'], null=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('event_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['masters.SessionType'])),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('start_time', self.gf('django.db.models.fields.TimeField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('end_time', self.gf('django.db.models.fields.TimeField')()),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('sms_content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('email_content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'Sessions', ['NewSession'])

        # Adding model 'Report'
        db.create_table(u'Sessions_report', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session_name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Sessions.NewSession'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('place', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('Duration', self.gf('django.db.models.fields.IntegerField')()),
            ('improvement', self.gf('django.db.models.fields.TextField')()),
            ('category', self.gf('django.db.models.fields.IntegerField')()),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'Sessions', ['Report'])

        # Adding M2M table for field center_name on 'Report'
        m2m_table_name = db.shorten_name(u'Sessions_report_center_name')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('report', models.ForeignKey(orm[u'Sessions.report'], null=False)),
            ('center', models.ForeignKey(orm[u'masters.center'], null=False))
        ))
        db.create_unique(m2m_table_name, ['report_id', 'center_id'])

        # Adding model 'SessionFlow'
        db.create_table(u'Sessions_sessionflow', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Sessions.Report'], null=True)),
            ('time', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('activity', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('details', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'Sessions', ['SessionFlow'])

        # Adding model 'SessionMedia'
        db.create_table(u'Sessions_sessionmedia', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Sessions.Report'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('category', self.gf('django.db.models.fields.IntegerField')()),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'Sessions', ['SessionMedia'])

        # Adding model 'Attendance'
        db.create_table(u'Sessions_attendance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Sessions.Report'], null=True)),
        ))
        db.send_create_signal(u'Sessions', ['Attendance'])

        # Adding M2M table for field ymht on 'Attendance'
        m2m_table_name = db.shorten_name(u'Sessions_attendance_ymht')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('attendance', models.ForeignKey(orm[u'Sessions.attendance'], null=False)),
            ('profile', models.ForeignKey(orm[u'profile.profile'], null=False))
        ))
        db.create_unique(m2m_table_name, ['attendance_id', 'profile_id'])

        # Adding model 'CoordinatorsAttendance'
        db.create_table(u'Sessions_coordinatorsattendance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Sessions.Report'], null=True)),
        ))
        db.send_create_signal(u'Sessions', ['CoordinatorsAttendance'])

        # Adding M2M table for field coordinators on 'CoordinatorsAttendance'
        m2m_table_name = db.shorten_name(u'Sessions_coordinatorsattendance_coordinators')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('coordinatorsattendance', models.ForeignKey(orm[u'Sessions.coordinatorsattendance'], null=False)),
            ('coordinator', models.ForeignKey(orm[u'masters.coordinator'], null=False))
        ))
        db.create_unique(m2m_table_name, ['coordinatorsattendance_id', 'coordinator_id'])


    def backwards(self, orm):
        # Deleting model 'NewSession'
        db.delete_table(u'Sessions_newsession')

        # Deleting model 'Report'
        db.delete_table(u'Sessions_report')

        # Removing M2M table for field center_name on 'Report'
        db.delete_table(db.shorten_name(u'Sessions_report_center_name'))

        # Deleting model 'SessionFlow'
        db.delete_table(u'Sessions_sessionflow')

        # Deleting model 'SessionMedia'
        db.delete_table(u'Sessions_sessionmedia')

        # Deleting model 'Attendance'
        db.delete_table(u'Sessions_attendance')

        # Removing M2M table for field ymht on 'Attendance'
        db.delete_table(db.shorten_name(u'Sessions_attendance_ymht'))

        # Deleting model 'CoordinatorsAttendance'
        db.delete_table(u'Sessions_coordinatorsattendance')

        # Removing M2M table for field coordinators on 'CoordinatorsAttendance'
        db.delete_table(db.shorten_name(u'Sessions_coordinatorsattendance_coordinators'))


    models = {
        u'Sessions.attendance': {
            'Meta': {'object_name': 'Attendance'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Sessions.Report']", 'null': 'True'}),
            'ymht': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['profile.Profile']", 'null': 'True', 'symmetrical': 'False'})
        },
        u'Sessions.coordinatorsattendance': {
            'Meta': {'object_name': 'CoordinatorsAttendance'},
            'coordinators': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['masters.Coordinator']", 'null': 'True', 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Sessions.Report']", 'null': 'True'})
        },
        u'Sessions.newsession': {
            'Meta': {'object_name': 'NewSession'},
            'age_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['masters.AgeGroup']", 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'email_content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'end_time': ('django.db.models.fields.TimeField', [], {}),
            'event_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['masters.SessionType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'sms_content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'start_time': ('django.db.models.fields.TimeField', [], {})
        },
        u'Sessions.report': {
            'Duration': ('django.db.models.fields.IntegerField', [], {}),
            'Meta': {'object_name': 'Report'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.IntegerField', [], {}),
            'center_name': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['masters.Center']", 'symmetrical': 'False'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'improvement': ('django.db.models.fields.TextField', [], {}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'session_name': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Sessions.NewSession']"})
        },
        u'Sessions.sessionflow': {
            'Meta': {'object_name': 'SessionFlow'},
            'activity': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'details': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Sessions.Report']", 'null': 'True'}),
            'time': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        },
        u'Sessions.sessionmedia': {
            'Meta': {'object_name': 'SessionMedia'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['Sessions.Report']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['masters.City']"}),
            'coordinators': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['masters.Coordinator']", 'symmetrical': 'False'}),
            'established_since': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'landmark': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'locality': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '6'})
        },
        u'masters.city': {
            'Meta': {'object_name': 'City'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['masters.State']"})
        },
        u'masters.coordinator': {
            'Meta': {'object_name': 'Coordinator'},
            'date_of_birth': ('django.db.models.fields.DateField', [], {}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'gnan_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'masters.hobby': {
            'Meta': {'object_name': 'Hobby'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
        },
        u'profile.profile': {
            'Meta': {'object_name': 'Profile'},
            'date_of_birth': ('django.db.models.fields.DateField', [], {}),
            'father_contact': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'father_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'male'", 'max_length': '25'}),
            'gnan_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'hobby': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['masters.Hobby']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'mother_contact': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'mother_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'profile_picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['Sessions']