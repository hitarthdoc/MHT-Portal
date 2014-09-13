from django.contrib import admin
from .models import AgeGroup, Role, SubRole, SessionType, Experience, JobType, City, State, Hobby, Center, GlobalEvent, LocalEvent, GNCSewa, Activities
from django_countries.fields import CountryField

admin.site.register(AgeGroup)
admin.site.register(Role)
admin.site.register(SessionType)
admin.site.register(Experience)
admin.site.register(JobType)
admin.site.register(City)
admin.site.register(State)
admin.site.register(Hobby)
admin.site.register(Center)
admin.site.register(GlobalEvent)
admin.site.register(LocalEvent)
admin.site.register(GNCSewa)
admin.site.register(Activities)
admin.site.register(SubRole)