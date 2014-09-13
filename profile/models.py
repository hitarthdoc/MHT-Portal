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
    user = models.OneToOneField(User, null=True, blank=True)
    first_name = models.CharField(max_length=255, validators=[RegexValidator(r'^[a-zA-Z]*$', 'Numbers are not allowed here.')])
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=25, blank=False, null=False, choices=GENDER_CHOICES, default='male')
    date_of_birth = models.DateField()
    hobby = models.ManyToManyField(Hobby, verbose_name='Hobbies')
    other_hobbies = models.CharField(max_length=50, blank=True,
	help_text="Only add hobbies here that are not listed in the Hobbies field above.")
    # event = models.ForeignKey(Event)
    gnan_date = models.DateField(blank=True, null=True)
    father_name = models.CharField(max_length=255)
    father_contact = models.CharField(max_length=10, blank=True, null=True, validators=[RegexValidator(r'^[0-9]*$', 'Only numbers are allowed here.')])
    mother_name = models.CharField(max_length=255)
    mother_contact = models.CharField(max_length=10, blank=True, null=True, validators=[RegexValidator(r'^[0-9]*$', 'Only numbers are allowed here.')])
    profile_picture = models.ImageField(upload_to=profile_picture_file_name, blank=True, null=True)

    # def prof_image(self):
    #   return '<img src="%s">' % (self.profile_picture)
    # prof_image.allow_tags = True

    class Meta:
        verbose_name_plural = 'Add New MHT'

    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)

    # class Meta:
    #   verbose_name_plural = "profile"
   
class YMHTMobile(models.Model):
    profile = models.ForeignKey(profile)
    mobile = models.CharField(max_length=10, validators=[RegexValidator(r'^[0-9]*$', 'Only numbers are allowed here.')])
    is_active = models.BooleanField(default=False)
  
    class Meta:
        verbose_name_plural = 'Mobile Details'

class YMHTEmail(models.Model):
    ymht = models.ForeignKey(profile)
    email = models.EmailField()
    is_active = models.BooleanField(default=False)
  
    class Meta:
        verbose_name_plural = 'Email Details'

class YMHTAddress(models.Model):
    ymht = models.ForeignKey(profile)
    address_1 = models.CharField(max_length=255)
    address_2 = models.CharField(max_length=255, blank=True, null=True)
    address_3 = models.CharField(max_length=255, blank=True, null=True)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    city = models.ForeignKey(City)
    zipcode = models.CharField(max_length=6, validators=[RegexValidator(r'^[0-9]*$', 'Only 6 numbers are allowed here.')])
    current_address = models.BooleanField(default=False)
  
    def __unicode__(self):
        return '%s' % (self.standard_or_Degree)
    class Meta:
        verbose_name_plural = 'Address Details'

class YMHTEducation(models.Model):
    Edu_choices = (
	  ('school', "School"),
	  ('college', "College"),)
    ymht = models.ForeignKey(profile)

    type_1 = models.CharField(choices=Edu_choices, max_length=256)
    school_or_College = models.CharField(max_length=255)
    standard_or_Degree = models.CharField(max_length=255)
    other_Details = models.TextField(null=True)
    year = models.CharField(max_length=255)

    def __unicode__(self):
        return '%s' % (self.standard_or_Degree)

    class Meta:
        verbose_name_plural = 'Education Details'

JOB_CHOICES = ((0, "BUSINESS"),
				(1, "JOB"),
				(2, "SERVICE"))

EXPERIENCE_CHOICES = ((0, "FRESHER"),
				(1, "1 YEAR"),
				(2, "2 YEAR"),
				(3, "3 YEAR"))

class YMHTJob(models.Model):
  ymht = models.ForeignKey(profile)
  jobtype = models.ForeignKey(JobType)
  experience = models.ForeignKey(Experience)
  company_name = models.CharField(max_length=255)
  designation = models.CharField(max_length=255)
  # job_category = models.CharField(max_length=255)
  current = models.BooleanField()

  def __unicode__(self):
	return '%s' % (self.company_name)

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
	return '%s, %s at %s center for age group %s' % (self.ymht, self.role, self.center, self.age_group)


class GlobalEventSewaDetails(models.Model):
  ATTENDED_DETAILS = ((1, 'All Days'), (2, 'Partial Days'))
  event = models.ForeignKey(GlobalEvent)
  ymht = models.ForeignKey(profile)
  attended = models.IntegerField(choices=ATTENDED_DETAILS)
  attended_days = models.IntegerField(blank=True, null=True)
  comments = models.CharField(max_length=100, blank=True, null=True)

  class Meta:
	  verbose_name_plural = 'Global Event Sewa Details'

class LocalEventSewaDetails(models.Model):
  ymht = models.ForeignKey(profile)
  event = models.ForeignKey(LocalEvent)
  sewa_dept = models.CharField(max_length=255)
  sewa_name = models.CharField(max_length=255)
  comments = models.CharField(max_length=100, blank=True, null=True)

  class Meta:
	  verbose_name_plural = 'Local Event Sewa Details'

class GNCSewaDetails(models.Model):
  ymht = models.ForeignKey(profile)
  name = models.ForeignKey(GNCSewa, null=True)
  project_responsible = models.CharField(max_length=255)
  comments = models.CharField(max_length=100, blank=True, null=True)

  class Meta:
	  verbose_name_plural = 'GNC Sewa Details'
