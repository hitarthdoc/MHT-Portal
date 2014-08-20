from django.db import models
from django.contrib.auth.models import User
from django.contrib.admin.widgets import ManyToManyRawIdWidget
from profile.models import Membership
from profile.models import Center
from profile.models import Profile
from masters.models import SessionType
from masters.models import AgeGroup
from masters.models import Coordinator
from django.core.exceptions import ValidationError

from datetime import datetime
import datetime as dt
#from datetime import time

def validate_time(value):
	earliest_time = dt.time(9)
	latest_time = dt.time(21)
	if value < earliest_time or value > latest_time:
		raise ValidationError(u'Please enter time between 9:00 AM and 9:00 PM')

def session_content_file_name(instance, filename):
    return '/'.join(['report', instance.Coordinators_present.user.username, filename])

def session_media_content_file_name(instance, filename):
    return '/'.join(['session_media', instance.session.Coordinators_present.user.username, filename])

class NewSession(models.Model):
#	EVENT_CHOICES = ((1, 'General Session'), (2, 'Special Session'), (3, 'Global Event'), (4, 'Local Event'))
	# AGE_GROUP_CHOICES = ((1, '13 to 16'), (2, '17 to 21'), (3, '13 to 21'), (4, '21 to 30'))

	def get_default_created_by():
		return Profile.objects.get(id=1)

	name = models.CharField(max_length=25)
	center_name = models.ManyToManyField(Center)
	age_group = models.ManyToManyField(AgeGroup, null=True)
	description = models.TextField(blank=True, null=True)
	event_type = models.ForeignKey(SessionType)
	start_date = models.DateField(default=datetime.today)
	#start_date = models.DateField()
	start_time = models.TimeField(validators=[validate_time], default=datetime.now)
	end_date = models.DateField(default=datetime.today)
	end_time = models.TimeField(validators=[validate_time], default=datetime.now)
	location = models.CharField(max_length=25)
	sms_content = models.TextField(verbose_name='SMS Content', null=True, blank=True, max_length = 160)
	email_subject = models.CharField(blank=True, null=True, max_length = 100)
	email_body = models.TextField(blank=True, null=True)
	# Foreign key to coordinator
	created_by = models.ForeignKey(User, default=get_default_created_by, null=True)
	approved = models.BooleanField(default=False)

	
	def __unicode__(self):
		return '%s on %s at %s.' % (self.name, self.start_date, self.location)

	#def __unicode__(self):
	#	return '%s, %s, %s: %s, %s, %s, %s, %s, %s' % (self.name, self.description, dict(EVENT_CHOICES).get(self.event_type), self.start_date, self.start_time, self.end_date, self.end_time, self.location, self._13_to_16_years, self._17_to_21_years)

	class Meta:
   		verbose_name_plural = 'Create New Session'

class Report(models.Model):
	
	def get_default_created_by():
		return Profile.objects.get(id=1)

	HOURS_CHOICES = ((1, '1 Hour'),(2, '2 Hour'),(3, '3 Hour'),(4, '4 Hour'),(5, '5 Hour'),(6, '6 Hour'))
	MIN_CHOICES = ((1, '0 Min'), (2, '15 Min'), (3, '30 Min'), (4, '45 Min'))

	session_name = models.ForeignKey(NewSession)
	date = models.DateField()
	place = models.CharField(max_length=255)
	Duration = models.IntegerField(choices=HOURS_CHOICES)
	improvement = models.TextField(verbose_name='Feedback / Improvements')

	CATEGORY_CHOICES = ((1, 'Photo'),
                      (2, 'Video'),
                      (3, 'Other'))

	category = models.IntegerField(choices=CATEGORY_CHOICES)
	attachment = models.FileField(upload_to=session_content_file_name, blank=True, null=True)
	created_by = models.ForeignKey(User, default=get_default_created_by, null=True)
	approved = models.NullBooleanField(default=False)


	def __unicode__(self):
		return '%s' % (self.session_name)

	class Meta:
   		verbose_name_plural = 'Create Session Report'


class SessionFlow(models.Model):
	session = models.ForeignKey(Report, null=True)
	time = models.CharField(max_length=255, null=True)
	activity = models.CharField(max_length=50)
	description = models.CharField(max_length=255)
	details = models.TextField()

class SessionMedia(models.Model):
  	session = models.ForeignKey(Report)
  	title = models.CharField(max_length=100, blank=True, null=True)

  	CATEGORY_CHOICES = ((1, 'Photo'),
                      	(2, 'Video'),
                      	(3, 'Other'))

  	category = models.IntegerField(choices=CATEGORY_CHOICES, null=True, blank=True)
  	attachment = models.FileField(upload_to=session_media_content_file_name, blank=True, null=True)

class Attendance(models.Model):
  
  	ymht = models.ManyToManyField(Profile, null=True)
  	session = models.ForeignKey(Report, null=True)

class CoordinatorsAttendance(models.Model):

	coords = models.ManyToManyField(Profile, null=True)

	#coordinators = models.ManyToManyField(Profile, null=True)
	session = models.ForeignKey(Report, null=True)
	class Meta:
   		verbose_name_plural = "Coordinator's Attendance"