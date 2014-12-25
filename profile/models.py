from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib import admin
import datetime
from django.core.validators import RegexValidator
from django_countries.fields import CountryField
from masters.models import City
from masters.models import State
from masters.models import AgeGroup
from masters.models import JobType
from masters.models import Experience
from masters.models import Role
from masters.models import SubRole
from masters.models import Hobby
from masters.models import Center
from masters.models import GlobalEvent
from masters.models import LocalEvent
from masters.models import GNCSewa

def profile_picture_file_name(instance, filename):
  try:
	return '/'.join(['profile', instance.user.username, filename])
  except:
	return '/'.join(['profile', 'YMHTians', filename])

EVENT_CATEGORY_CHOICES = ((0, 'GNC Day'),
	  (1, 'Summer Camp'),
	  (2, 'YUVA Camp'),
	  (3, 'Aptaputra Satsang'),
	  (4, 'General Satsang'),
	  (5, 'Parayan'),
	  (6, 'Janma Jayanti'),
	  (7, 'Picnic'))

class profile(models.Model):

	description = "Add/edit profiles of MHTs"

	GENDER_CHOICES = (
	('male', "Male"),
	('female', "Female"),)
	user = models.OneToOneField(User, null=True, blank=True,
  help_text="Please select user only for Helpers and Coordinators. In case of Participants, please leave this field blank.")
	first_name = models.CharField(max_length=255, validators=[RegexValidator(r'^[a-zA-Z]*$', 'Numbers are not allowed here.')])
	last_name = models.CharField(max_length=255)
	gender = models.CharField(max_length=25, blank=False, null=False, choices=GENDER_CHOICES, default='male')
	date_of_birth = models.DateField(help_text="Date Format: DD-MM-YYYY")
	hobby = models.ManyToManyField(Hobby, verbose_name='Hobbies')
	other_hobbies = models.CharField(max_length=50, blank=True,
  help_text="Only add hobbies here that are not listed in the Hobbies field above.")
	# event = models.ForeignKey(Event)
	gnan_date = models.DateField(blank=True, null=True, help_text="Date Format: DD-MM-YYYY")
	father_name = models.CharField(max_length=255, verbose_name="Father's name")
	father_contact = models.CharField(max_length=10, blank=True, null=True, verbose_name="Father's contact", validators=[RegexValidator(r'^[0-9]*$', 'Only numbers are allowed here.')])
	mother_name = models.CharField(max_length=255, verbose_name="Mother's name")
	mother_contact = models.CharField(max_length=10, blank=True, null=True, verbose_name="Mother's contact", validators=[RegexValidator(r'^[0-9]*$', 'Only numbers are allowed here.')])
	profile_picture = models.ImageField(upload_to=profile_picture_file_name, blank=True, null=True)

  # def prof_image(self):
  #   return '<img src="%s">' % (self.profile_picture)
  # prof_image.allow_tags = True

	class Meta:
		verbose_name_plural = 'Profile'

	def __unicode__(self):
		return '%s %s' % (self.first_name, self.last_name)

  # class Meta:
  #   verbose_name_plural = "profile"
	 
class YMHTMobile(models.Model):
	profile = models.ForeignKey(profile)
	mobile = models.CharField(max_length=10, validators=[RegexValidator(r'^[0-9]*$', 'Only numbers are allowed here.')])
	is_active = models.BooleanField(default=False)
	
	def __unicode__(self):
		return '%s' % self.mobile

	class Meta:
		verbose_name_plural = 'Mobile Details'

class YMHTEmail(models.Model):
	ymht = models.ForeignKey(profile)
	email = models.EmailField()
	is_active = models.BooleanField(default=False)

	def __unicode__(self):
		return '%s' % self.email
	class Meta:
		verbose_name_plural = 'Email Details'

class YMHTAddress(models.Model):
	ymht = models.ForeignKey(profile)
	address_1 = models.CharField(max_length=255)
	address_2 = models.CharField(max_length=255, blank=True, null=True)
	address_3 = models.CharField(max_length=255, blank=True, null=True)
	landmark = models.CharField(max_length=255, blank=True, null=True)
	city = models.ForeignKey(City)
	zipcode = models.CharField(max_length=6, validators=[RegexValidator(r'^[0-9]*$',
		'Only 6 digits are allowed here.')])
	current_address = models.BooleanField(default=False)

	def __unicode__(self):
		return "%s, %s" % (self.address_1, self.city)

	class Meta:
		verbose_name_plural = 'Address Details'

class YMHTEducation(models.Model):
	Edu_choices = (
	  ('school', "School"),
	  ('college', "College"),)
	ymht = models.ForeignKey(profile)
	school_or_College = models.CharField(choices=Edu_choices, max_length=256)
	institution_name = models.CharField(max_length=255, verbose_name="School/College Name:")
	stream_or_Degree = models.CharField(max_length=255, null=True, verbose_name="Stream/Degree",
		help_text="E.g. Science, Commerce, Arts, B.E., Diploma. Use None in case of no stream.")
	class_or_year = models.CharField(max_length=255, null=True, verbose_name="Standard/Year")
	other_Details = models.TextField(blank=True, null=True, help_text="Any other remarks")
	current = models.BooleanField(default=False)
	def __unicode__(self):
		return 'Year/Class:%s, %s, %s' % (self.class_or_year, self.stream_or_Degree,
			self.institution_name)

	class Meta:
  		verbose_name_plural = 'Education Details'

class YMHTJob(models.Model):
	ymht = models.ForeignKey(profile)
	job_type = models.ForeignKey(JobType, null=True)
	experience = models.ForeignKey(Experience)
	company_name = models.CharField(max_length=255)
	designation = models.CharField(max_length=255)
	# job_category = models.CharField(max_length=255)
	current = models.BooleanField()

	def __unicode__(self):
		return '%s, %s at %s' % (self.job_type, self.designation, self.company_name)

	class Meta:
		verbose_name_plural = 'Job Details' 

class Membership(models.Model):
	ymht = models.ForeignKey(profile)
	center = models.ForeignKey(Center, null=True)
	age_group = models.ForeignKey(AgeGroup)
	role = models.ForeignKey(Role)
	sub_role = models.ManyToManyField(SubRole, blank=True)
	since = models.DateField()
	till = models.DateField(blank=True, null=True)
	is_active = models.BooleanField(default=False)

	def __unicode__(self):
		return '%s, %s at %s center for age group %s' % (self.ymht, self.role, self.center,
			self.age_group) 


class GlobalEventSewaDetails(models.Model):
	ATTENDED_DETAILS = ((1, 'All Days'), (2, 'Partial Days'))
	ymht = models.ForeignKey(profile)
	event = models.ForeignKey(GlobalEvent)
	department = models.CharField(max_length=50, null=True)
	attended = models.IntegerField(choices=ATTENDED_DETAILS)
	attended_days = models.IntegerField(blank=True, null=True)
	comments = models.CharField(max_length=100, blank=True, null=True)

	def __unicode__(self):
		return "%s" % (self.event)
	class Meta:
		verbose_name_plural = 'Global Event Sewa Details'

class LocalEventSewaDetails(models.Model):
	ymht = models.ForeignKey(profile)
	event = models.ForeignKey(LocalEvent)
	sewa_dept = models.CharField(max_length=255)
	sewa_name = models.CharField(max_length=255, null = True, editable=False)
	comments = models.CharField(max_length=100, blank=True, null=True)

	def __unicode__(self):
		return "%s, %s" % (self.sewa_dept, self.event)
	class Meta:
		verbose_name_plural = 'Local Event Sewa Details'

class GNCSewaDetails(models.Model):
	ymht = models.ForeignKey(profile)
	name = models.ForeignKey(GNCSewa, null=True)
	project_responsible = models.CharField(max_length=255, verbose_name='Coordinator name',
# 	coordinator_name = models.CharField(max_length=255, null=True,
        help_text="Person who is responsible for the project")
	comments = models.CharField(max_length=100, blank=True, null=True)

	def __unicode__(self):
		return "%s" % (self.name)
	class Meta:
		verbose_name_plural = 'GNC Sewa Details'
