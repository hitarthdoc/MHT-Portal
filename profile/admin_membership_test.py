from django.contrib import admin
# Please refer to this site for explanation of why this is done:
from django.db.models import Q
from operator import __or__ as OR
from itertools import chain
# http://simeonfranklin.com/blog/2011/jun/14/best-way-or-list-django-orm-q-objects/
from profile.models import Membership, Center, profile
from masters.models import Role
from .models import (profile, YMHTMobile,
                    YMHTEmail, YMHTAddress, YMHTEducation, YMHTJob,
                    Membership,
                    GNCSewaDetails, LocalEventSewaDetails, GlobalEventSewaDetails)
from Sessions.models import *
from django_countries.fields import CountryField
from django import forms

class YMHTMembershipInline(admin.StackedInline):
    fields = ('ymht' , 'center' , 'age_group' , 'role', 'since', 'till', 'is_active')
    model = Membership
    formset = RequiredFormSet
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
