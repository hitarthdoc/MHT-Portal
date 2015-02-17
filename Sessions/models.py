from django.db import models
from django.contrib.auth.models import User
from profile.models import Center
from profile.models import profile
from masters.models import SessionType
from masters.models import AgeGroup
from masters.models import Activities
# from django.core.exceptions import ValidationError

from datetime import datetime


def session_content_file_name(instance, filename):
    return '/'.join(['report', instance.created_by.username, filename])


def session_media_content_file_name(instance, filename):
    return '/'.join(['session_media', instance.session.created_by.username,
                    filename])


class NewSession(models.Model):

    def get_default_created_by():
        try:
            return User.objects.get(id=1)
        except:
            return User.objects.none()

    name = models.CharField(max_length=25)
    center_name = models.ManyToManyField(Center)
    age_group = models.ManyToManyField(AgeGroup, null=True)
    description = models.TextField(blank=True, null=True)
    event_type = models.ForeignKey(SessionType)
    start_date = models.DateField(default=datetime.today)
    start_time = models.TimeField(default=datetime.now)
    end_date = models.DateField(default=datetime.today)
    end_time = models.TimeField(default=datetime.now)
    location = models.CharField(max_length=25)
    sms_content = models.TextField(verbose_name='SMS Content', null=True,
                                   blank=True, max_length=160)
    email_subject = models.CharField(blank=True, null=True, max_length=100)
    email_body = models.TextField(blank=True, null=True)
    # Foreign key to coordinator
    created_by = models.ForeignKey(User, default=get_default_created_by,
                                   null=True)
    # last_editted_by = models.ForeignKey(User, default=get_default_created_by,
    # null=True)
    approved = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s on %s at %s.' % (self.name, self.start_date, self.location)
    # TODO: Above statement does not print the proper center name because it is
    # a manytomany field

    class Meta:
        verbose_name_plural = 'Sessions'


class Report(models.Model):

    def get_default_created_by():
        try:
            return User.objects.get(id=1)
        except:
            return User.objects.none()

    HOURS_CHOICES = ((1, '1 Hour'), (2, '2 Hour'), (3, '3 Hour'), (4, '4 Hour'),
                     (5, '5 Hour'), (6, '6 Hour'))
    MIN_CHOICES = ((1, '0 Min'), (2, '15 Min'), (3, '30 Min'), (4, '45 Min'))

    session_name = models.ForeignKey(NewSession)
#   date = models.DateField(blank=True,)# default="2014-1-1")
# TODO: Fetch date, place, Duration from session name and display here as
# editable or read-only

    improvement = models.TextField(verbose_name='Feedback/Improvements',
                                   blank=True)

    CATEGORY_CHOICES = (('P', 'Photo'),
                        ('V', 'Video'),
                        ('D', 'Document'),
                        ('O', 'Other'))

    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2, blank=True,
                                verbose_name='Category of Attachment (if any)')
    attachment = models.FileField(upload_to=session_content_file_name, blank=True, null=True)
    created_by = models.ForeignKey(User, default=get_default_created_by, null=True)
    approved = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s' % (self.session_name)

    class Meta:
        verbose_name_plural = 'Session Reports'


class SessionFlow(models.Model):
    session = models.ForeignKey(Report, null=True)
    # Edit here
    time = models.IntegerField(verbose_name="Time (Minutes)", null=True, blank=True)
    activity = models.ForeignKey(Activities)
    description = models.CharField(max_length=255, null=True, blank=True)
    details = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Session flow"


class SessionMedia(models.Model):

    session = models.ForeignKey(Report)
    title = models.CharField(max_length=100, blank=True, null=True)

    CATEGORY_CHOICES = (('P', 'Photo'),
                        ('V', 'Video'),
                        ('O', 'Other'))

    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2, null=True, blank=True,)
    attachment = models.FileField(upload_to=session_media_content_file_name, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Session Media"


class Attendance(models.Model):
    attendance_name = "Attendance"
    # TODO: Change wherever there is ymht to either profile or MHT for further expansion
    ymht = models.ManyToManyField(profile, null=True, verbose_name='MHTs')
    session = models.ForeignKey(Report, null=True)

    class Meta:
        verbose_name_plural = "Attendance"
    def __unicode__(self):
        return '%s' % (self.attendance_name)


class CoordinatorsAttendance(models.Model):
    coords_name = "Coordinators' Attendance"
    coords = models.ManyToManyField(profile, null=True, verbose_name='Coordinators')

    # coordinators = models.ManyToManyField(profile, null=True)
    session = models.ForeignKey(Report, null=True)

    class Meta:
        verbose_name_plural = "Coordinator's Attendance"
    def __unicode__(self):
        return '%s' % (self.coords_name)