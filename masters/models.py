from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.core.validators import RegexValidator


class AgeGroup(models.Model):

    age_group = models.CharField(blank=True, null=False, max_length=255)

    def __unicode__(self):
        return '%s' % (self.age_group)

    class Meta:
        verbose_name_plural = 'Age group'


class Role(models.Model):

    level = models.IntegerField(null=True)
    role = models.CharField(blank=True, null=False, max_length=255)

    def __unicode__(self):
        return '%s' % (self.role)


class SubRole(models.Model):

    role = models.ForeignKey(Role)
    sub_role = models.CharField(max_length=52)

    def __unicode__(self):
        return '%s - %s' % (self.sub_role, self.role)


class SessionType(models.Model):

    session_type = models.CharField(blank=True, null=False, max_length=255)

    def __unicode__(self):
        return '%s' % (self.session_type)


class Activities(models.Model):

    activities = models.CharField(blank=True, null=False, max_length=255)

    def __unicode__(self):
        return '%s' % (self.activities)

    class Meta:
        verbose_name_plural = 'Activities'


class Experience(models.Model):

    experience = models.CharField(blank=True, null=True, max_length=63)

    def __unicode__(self):
        return '%s' % (self.experience)


class JobType(models.Model):

    job_type = models.CharField(blank=True, null=True, max_length=255)

    def __unicode__(self):
        return '%s' % (self.job_type)


class State(models.Model):

    name = models.CharField(max_length=255)
    country = CountryField()

    def __unicode__(self):
        return '%s, %s' % (self.name, self.country)


class City(models.Model):

    name = models.CharField(max_length=255)
    state = models.ForeignKey(State)

    def __unicode__(self):
        return '%s, %s' % (self.name, self.state)

    class Meta:
        verbose_name_plural = 'City'


class Hobby(models.Model):

    title = models.CharField(max_length=255)

    def __unicode__(self):
        return '%s' % (self.title)

    class Meta:
        verbose_name_plural = 'Hobbies'


class Center(models.Model):

    CATEGORY_CHOICES = ((1, 'BMHT'),
                        (2, 'LMHT'),
                        (3, 'YMHT'))
    category = models.IntegerField(choices=CATEGORY_CHOICES)
    established_since = models.DateField()
    center_name = models.CharField(max_length=255, null=True)
    address_1 = models.CharField(max_length=255)
    address_2 = models.CharField(max_length=255, blank=True, null=True)
    address_3 = models.CharField(max_length=255, blank=True, null=True)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    city = models.ForeignKey(City)
    zipcode = models.CharField(max_length=6, validators=[RegexValidator(r'^[0-9]*$', 'Only numbers are allowed here.')])

    def __unicode__(self):
        return '%s, %s' % (self.center_name, self.city)


class GlobalEvent(models.Model):

    name = models.CharField(max_length=255)

    def __unicode__(self):
        return '%s' % (self.name)


class LocalEvent(models.Model):

    name = models.CharField(max_length=255)

    def __unicode__(self):
        return '%s' % (self.name)


class GNCSewa(models.Model):

    name = models.CharField(max_length=255, null=True)

    def __unicode__(self):
        return '%s' % (self.name)
