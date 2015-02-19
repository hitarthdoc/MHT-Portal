# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'profile'
        db.create_table(u'profile_profile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, null=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('gender', self.gf('django.db.models.fields.CharField')(default='male', max_length=25)),
            ('date_of_birth', self.gf('django.db.models.fields.DateField')()),
            ('other_hobbies', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('gnan_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('father_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('father_contact', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('mother_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('mother_contact', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('profile_picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'profile', ['profile'])

        # Adding M2M table for field hobby on 'profile'
        m2m_table_name = db.shorten_name(u'profile_profile_hobby')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('profile', models.ForeignKey(orm[u'profile.profile'], null=False)),
            ('hobby', models.ForeignKey(orm[u'masters.hobby'], null=False))
        ))
        db.create_unique(m2m_table_name, ['profile_id', 'hobby_id'])

        # Adding model 'YMHTMobile'
        db.create_table(u'profile_ymhtmobile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profile.profile'])),
            ('mobile', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'profile', ['YMHTMobile'])

        # Adding model 'YMHTEmail'
        db.create_table(u'profile_ymhtemail', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profile.profile'])),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'profile', ['YMHTEmail'])

        # Adding model 'YMHTAddress'
        db.create_table(u'profile_ymhtaddress', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profile.profile'])),
            ('address_1', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('address_2', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('address_3', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('landmark', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['masters.City'])),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('current_address', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'profile', ['YMHTAddress'])

        # Adding model 'YMHTEducation'
        db.create_table(u'profile_ymhteducation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profile.profile'])),
            ('school_or_College', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('institution_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('stream_or_Degree', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('class_or_year', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('other_Details', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('current', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'profile', ['YMHTEducation'])

        # Adding model 'YMHTJob'
        db.create_table(u'profile_ymhtjob', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profile.profile'])),
            ('job_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['masters.JobType'], null=True)),
            ('experience', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['masters.Experience'])),
            ('company_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('designation', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('current', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'profile', ['YMHTJob'])

        # Adding model 'Membership'
        db.create_table(u'profile_membership', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profile.profile'])),
            ('center', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['masters.Center'], null=True)),
            ('age_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['masters.AgeGroup'])),
            ('role', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['masters.Role'])),
            ('since', self.gf('django.db.models.fields.DateField')()),
            ('till', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'profile', ['Membership'])

        # Adding M2M table for field sub_role on 'Membership'
        m2m_table_name = db.shorten_name(u'profile_membership_sub_role')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('membership', models.ForeignKey(orm[u'profile.membership'], null=False)),
            ('subrole', models.ForeignKey(orm[u'masters.subrole'], null=False))
        ))
        db.create_unique(m2m_table_name, ['membership_id', 'subrole_id'])

        # Adding model 'GlobalEventSewaDetails'
        db.create_table(u'profile_globaleventsewadetails', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profile.profile'])),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['masters.GlobalEvent'])),
            ('department', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('attended', self.gf('django.db.models.fields.IntegerField')()),
            ('attended_days', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('comments', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'profile', ['GlobalEventSewaDetails'])

        # Adding model 'LocalEventSewaDetails'
        db.create_table(u'profile_localeventsewadetails', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profile.profile'])),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['masters.LocalEvent'])),
            ('sewa_dept', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('sewa_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('comments', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'profile', ['LocalEventSewaDetails'])

        # Adding model 'GNCSewaDetails'
        db.create_table(u'profile_gncsewadetails', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profile.profile'])),
            ('name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['masters.GNCSewa'], null=True)),
            ('project_responsible', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('comments', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'profile', ['GNCSewaDetails'])


    def backwards(self, orm):
        # Deleting model 'profile'
        db.delete_table(u'profile_profile')

        # Removing M2M table for field hobby on 'profile'
        db.delete_table(db.shorten_name(u'profile_profile_hobby'))

        # Deleting model 'YMHTMobile'
        db.delete_table(u'profile_ymhtmobile')

        # Deleting model 'YMHTEmail'
        db.delete_table(u'profile_ymhtemail')

        # Deleting model 'YMHTAddress'
        db.delete_table(u'profile_ymhtaddress')

        # Deleting model 'YMHTEducation'
        db.delete_table(u'profile_ymhteducation')

        # Deleting model 'YMHTJob'
        db.delete_table(u'profile_ymhtjob')

        # Deleting model 'Membership'
        db.delete_table(u'profile_membership')

        # Removing M2M table for field sub_role on 'Membership'
        db.delete_table(db.shorten_name(u'profile_membership_sub_role'))

        # Deleting model 'GlobalEventSewaDetails'
        db.delete_table(u'profile_globaleventsewadetails')

        # Deleting model 'LocalEventSewaDetails'
        db.delete_table(u'profile_localeventsewadetails')

        # Deleting model 'GNCSewaDetails'
        db.delete_table(u'profile_gncsewadetails')


    models = {
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
            'experience': ('django.db.models.fields.CharField', [], {'max_length': '63', 'null': 'True', 'blank': 'True'}),
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
        u'masters.state': {
            'Meta': {'object_name': 'State'},
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'masters.subrole': {
            'Meta': {'object_name': 'SubRole'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['masters.Role']"}),
            'sub_role': ('django.db.models.fields.CharField', [], {'max_length': '52'})
        },
        u'profile.globaleventsewadetails': {
            'Meta': {'object_name': 'GlobalEventSewaDetails'},
            'attended': ('django.db.models.fields.IntegerField', [], {}),
            'attended_days': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'department': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['masters.GlobalEvent']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['profile.profile']"})
        },
        u'profile.gncsewadetails': {
            'Meta': {'object_name': 'GNCSewaDetails'},
            'comments': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['masters.GNCSewa']", 'null': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['profile.profile']"}),
            'project_responsible': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'profile.localeventsewadetails': {
            'Meta': {'object_name': 'LocalEventSewaDetails'},
            'comments': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['masters.LocalEvent']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['profile.profile']"}),
            'sewa_dept': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sewa_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        },
        u'profile.membership': {
            'Meta': {'object_name': 'Membership'},
            'age_group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['masters.AgeGroup']"}),
            'center': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['masters.Center']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['profile.profile']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['masters.Role']"}),
            'since': ('django.db.models.fields.DateField', [], {}),
            'sub_role': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['masters.SubRole']", 'symmetrical': 'False', 'blank': 'True'}),
            'till': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        u'profile.profile': {
            'Meta': {'object_name': 'profile'},
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
            'other_hobbies': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'profile_picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'profile.ymhtaddress': {
            'Meta': {'object_name': 'YMHTAddress'},
            'address_1': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'address_2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'address_3': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['masters.City']"}),
            'current_address': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'landmark': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['profile.profile']"}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '6'})
        },
        u'profile.ymhteducation': {
            'Meta': {'object_name': 'YMHTEducation'},
            'class_or_year': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'current': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'other_Details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['profile.profile']"}),
            'school_or_College': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'stream_or_Degree': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        },
        u'profile.ymhtemail': {
            'Meta': {'object_name': 'YMHTEmail'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['profile.profile']"})
        },
        u'profile.ymhtjob': {
            'Meta': {'object_name': 'YMHTJob'},
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'current': ('django.db.models.fields.BooleanField', [], {}),
            'designation': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'experience': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['masters.Experience']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['masters.JobType']", 'null': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['profile.profile']"})
        },
        u'profile.ymhtmobile': {
            'Meta': {'object_name': 'YMHTMobile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['profile.profile']"})
        }
    }

    complete_apps = ['profile']