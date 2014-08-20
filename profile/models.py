from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib import admin
import datetime
from django.core.validators import RegexValidator
from django_countries.fields import CountryField
from masters.models import City, State, AgeGroup, JobType, Experience, Role, Hobby, Coordinator, Center, GlobalEvent, LocalEvent, GNCSewa


def session_content_file_name(instance, filename):
    return '/'.join(['session', instance.user.username, filename])

EVENT_CATEGORY_CHOICES = ((0, 'GNC Day'),
                    (1, 'Summer Camp'),
                    (2, 'YUVA Camp'),
                    (3, 'Aptaputra Satsang'),
                    (4, 'General Satsang'),
                    (5, 'Parayan'),
                    (6, 'Janma Jayanti'),
                    (7, 'Picnic'))

class Profile(models.Model):
  GENDER_CHOICES = (
      ('male', "Male"),
      ('female', "Female"),)
  user = models.OneToOneField(User, null=True, blank=True)
  first_name = models.CharField(max_length=255, validators=[RegexValidator(r'^[a-zA-Z]*$','Numbers are not allowed here.')])
  last_name = models.CharField(max_length=255)
  gender = models.CharField(max_length=25, blank=False, null=False, choices=GENDER_CHOICES, default='male')
  date_of_birth = models.DateField()
  hobby = models.ManyToManyField(Hobby)
  #event = models.ForeignKey(Event)
  gnan_date = models.DateField(blank=True, null=True)
  father_name = models.CharField(max_length=255)
  father_contact = models.CharField(max_length=10, blank=True, null=True, validators=[RegexValidator(r'^[0-9]*$','Only numbers are allowed here.')])
  mother_name = models.CharField(max_length=255)
  mother_contact = models.CharField(max_length=10, blank=True, null=True, validators=[RegexValidator(r'^[0-9]*$','Only numbers are allowed here.')])
  profile_picture = models.ImageField(upload_to=session_content_file_name, blank=True, null=True)

  # def prof_image(self):
  #   return '<img src="%s">' % (self.profile_picture)
  # prof_image.allow_tags = True

  def __unicode__(self):
    return '%s %s' % (self.first_name, self.last_name)

  # class Meta:
  #   verbose_name_plural = "Profile"
   
class YMHTMobile(models.Model):
  profile = models.ForeignKey(Profile)
  mobile = models.CharField(max_length=10, validators=[RegexValidator(r'^[0-9]*$','Only numbers are allowed here.')])
  is_active = models.BooleanField(default=False)
  
  class Meta:
    verbose_name_plural = 'Mobile Details'

class YMHTEmail(models.Model):
  ymht = models.ForeignKey(Profile)
  email = models.EmailField()
  is_active = models.BooleanField(default=False)
  
  class Meta:
    verbose_name_plural = 'Email Details'

class YMHTAddress(models.Model):
  ymht = models.ForeignKey(Profile)
  address_1 = models.CharField(max_length=255, null=False)
  address_2 = models.CharField(max_length=255, blank=True, null=True)
  address_3 = models.CharField(max_length=255, blank=True, null=True)
  landmark = models.CharField(max_length=255, blank=True, null=True)
  city = models.ForeignKey(City)
  zipcode = models.CharField(max_length=6, validators=[RegexValidator(r'^[0-9]*$','Only 6 numbers are allowed here.')])
  current_address = models.BooleanField(default=False)
  
  class Meta:
    verbose_name_plural = 'Address Details'

class YMHTEducation(models.Model):
  Edu_choices = (
      ('school', "school"),
      ('college', "college"),)
  ymht = models.ForeignKey(Profile)

  type_1 = models.CharField(choices=Edu_choices, max_length=256)
  school_or_College = models.CharField(max_length=255)
  standard_or_Degree = models.CharField(max_length=255)
  other_Details = models.TextField(null=True)
  year = models.CharField(max_length=255)

  def __unicode__(self):
    return '%s' % (self.standard_or_Degree)

  class Meta:
    verbose_name_plural = 'Education Details'

JOB_CHOICES = ((0,"BUSINESS"),
                (1,"JOB"),
                (2,"SERVICE"))

EXPERIENCE_CHOICES = ((0,"FRESHER"),
                (1,"1 YEAR"),
                (2,"2 YEAR"),
                (3,"3 YEAR"))

class YMHTJob(models.Model):
  ymht = models.ForeignKey(Profile)
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

  def get_center_default():
    return Profile.objects.get(id=1)

  ROLE_CHOICES = ((1, 'Participant'),
                  (2, 'Coordinator'),
                  (3, 'Helper'))
  ymht = models.ForeignKey(Profile, null=False, blank=False)
  center = models.ForeignKey(Center, null=False,blank=False)
  age_group = models.ForeignKey(AgeGroup, null=False, blank=False)
  role = models.ForeignKey(Role, null=False)
  since = models.DateField(null=False)
  till = models.DateField(null=True, blank=True)
  is_active = models.BooleanField(default=False)

  def __unicode__(self):
    return '%s, %s at %s center for age group %s' % (self.ymht, self.role, self.center, self.age_group)


class GlobalEventSewaDetails(models.Model):
  ATTENDED_DETAILS = ((1, 'All Days'), (2, 'Partial Days'))
  event = models.ForeignKey(GlobalEvent)
  ymht = models.ForeignKey(Profile)
  attended = models.IntegerField(choices=ATTENDED_DETAILS)
  attended_days = models.IntegerField(blank=True, null=True)
  comments = models.CharField(max_length=100, blank=True, null=True)

  class Meta:
      verbose_name_plural = 'Global Event Sewa Details'

class LocalEventSewaDetails(models.Model):
  ymht = models.ForeignKey(Profile)
  event = models.ForeignKey(LocalEvent)
  sewa_dept = models.CharField(max_length=255)
  sewa_name = models.CharField(max_length=255)
  comments = models.CharField(max_length=100, blank=True, null=True)

  class Meta:
      verbose_name_plural = 'Local Event Sewa Details'

class GNCSewaDetails(models.Model):
  ymht = models.ForeignKey(Profile)
  name = models.ForeignKey(GNCSewa, null=True)
  project_responsible = models.CharField(max_length=255)
  comments = models.CharField(max_length=100, blank=True, null=True)

  class Meta:
      verbose_name_plural = 'GNC Sewa Details'
