from operator import __or__ as OR
from django.contrib import admin
from django.db import models
from django.forms import TextInput, Textarea
from django.forms import CheckboxSelectMultiple, SelectMultiple
from .models import *
from profile.models import Membership, profile, Center, Role
from actions import export_as_csv
from constants import *

#was accessing from constants until 10:30 PM, 14/2/2015, hence temporarily moved
PARTICIPANT_ROLE_LEVEL = 1
HELPER_ROLE_LEVEL = 2
COORD_ROLE_LEVEL = 3


def get_current_user_details(user):
    current_profile = profile.objects.get(user=user)
    current_members = Membership.objects.filter(ymht=current_profile)
    current_centers = []
    current_age_groups = []
    for member in current_members:
        if member.is_active:
            current_centers.append(member.center)
            current_age_groups.append(member.age_group)
    return current_profile, current_members, current_centers, current_age_groups


# def return_status(request, fields, obj=None, readonly_fields=()):
# def get_readonly_fields(fields, request, obj=None):
#   Both these functions are defined in py  


class SessionFlowInline(admin.TabularInline):
    model = SessionFlow
    fields = ('session', 'time', 'activity', 'description', 'details')
    extra = 1
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }

    def get_readonly_fields(self, request, obj=None):
        return global_get_readonly_fields(self, request, obj)


class SessionMediaInline(admin.TabularInline):
    model = SessionMedia
    fields = ('session', 'title', 'category', 'attachment',)
    extra = 1

    def get_readonly_fields(self, request, obj=None):
        return global_get_readonly_fields(self, request, obj)


class AttendanceInline(admin.TabularInline):
    model = Attendance
    fields = ('ymht',)
    filter_horizontal = ("ymht",)
    extra = 1
    max_num = 1
    can_delete = False
    actions = [export_as_csv]

    def get_readonly_fields(self, request, obj=None):
        return global_get_readonly_fields(self, request, obj)

    # TODO: Change the size of manytomany widget because attendance manytomany field is very small

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # pnh_members represents Memberships of Participants and helpers
        if db_field.name == 'ymht':
            # pnh_members represents Memberships of Participants and helpers
            pnh_members = Membership.objects.filter(role__level__lt=COORD_ROLE_LEVEL)
            if profile.objects.filter(user=request.user).exists():
            # If profile for the current user exists, then this part is executed
                current_profile, current_members, current_centers, current_age_groups = get_current_user_details(request.user)
                pnh_members = pnh_members.filter(is_active=True, center__in=current_centers,
                                                 age_group__in=current_age_groups)
            # distinct is used because the above line may return duplicate profiles
            participant_profiles = profile.objects.filter(membership__in=pnh_members)        
            # distinct is used because the above line may return duplicate profiles
            kwargs['queryset'] = participant_profiles.distinct()
        return super(AttendanceInline, self).formfield_for_manytomany(db_field, request, **kwargs)


class CoordAttendanceInline(admin.TabularInline):
    model = CoordinatorsAttendance
    fields = ('coords',)
    filter_horizontal = ("coords",)
    max_num = 1
    extra = 1
    can_delete = False
    actions = [export_as_csv]

    def get_readonly_fields(self, request, obj=None):
        return global_get_readonly_fields(self, request, obj)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'coords':
            coords_members = Membership.objects.filter(role__level=COORD_ROLE_LEVEL)
            if profile.objects.filter(user=request.user).exists():
                current_profile, current_members, current_centers, current_age_groups = get_current_user_details(request.user)
                coords_members = coords_members.filter(center__in=current_centers,
                                                       age_group__in=current_age_groups)
            coords_profiles = profile.objects.filter(membership__in=coords_members)
            kwargs['queryset'] = coords_profiles.distinct()
        return super(CoordAttendanceInline, self).formfield_for_manytomany(db_field, request, **kwargs)


class ReportAdmin(admin.ModelAdmin):
    inlines = [
        SessionFlowInline,
        SessionMediaInline,
        AttendanceInline,
        CoordAttendanceInline,
    ]
    fields = ('session_name', 'improvement', 'category', 'attachment', 'created_by', 'approved')
    list_display = ('session_name', 'created_by', 'approved')
    # TODO: If the coordinator of the report opens the report, then it should not
    # be read only. All other fields of other inlines e.g. Attendance, media should
    # also be read only
    # formfield_overrides = {models.ManyToManyField: {'widget': SelectMultiple(attrs={'size': '10'})}, }
    
    def get_readonly_fields(self, request, obj=None):
        user_is_coord_of_current_center = False
        status = return_status(request, obj)
        result = {
                'Superuser': [],
                'Other User': self.readonly_fields + self.fields,
                'Center Coordinator': ['created_by'],
                'New Object': [],
            }[status]
        return result

    def queryset(self, request):
        qs = super(ReportAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs

        approved_qs = qs.filter(approved=True)

        # If profile or Membership of the current user does not exist, return only approved_qs
        if not (profile.objects.filter(user=request.user).exists() and 
                Membership.objects.filter(is_active=True, ymht=profile.objects.get(user=request.user)).exists()):
            return approved_qs

        current_profile, current_members, current_centers, current_age_groups = get_current_user_details(request.user)

        filtered_qs = qs.filter(session_name__center_name__in=current_centers, session_name__age_group__in=current_age_groups)
        # The queryset should include both approved reports from all centers
        # and also report of one's own center
        return reduce(OR, [approved_qs, filtered_qs])
    
    # TODO: Cleanup from here

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            return super(ReportAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
# If profile for current user does not exist, then what to do?
        if not profile.objects.filter(user=request.user).exists():
            return super(ReportAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

        current_profile = profile.objects.get(user=request.user)
        current_members = Membership.objects.filter(ymht=current_profile)
        current_centers_pk = []
        for member in current_members:
            if member.is_active:
                current_centers_pk.append(member.center.pk)
        if db_field.name == 'center_name':
            kwargs['queryset'] = Center.objects.filter(pk__in=current_centers_pk)
        return super(ReportAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            return super(ReportAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if not profile.objects.filter(user=request.user).exists():
            return super(ReportAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

        current_profile = profile.objects.get(user=request.user)
        current_members = Membership.objects.filter(ymht=current_profile)
        current_centers = []
        current_age_groups = []
        for member in current_members:
            if member.is_active:
                current_centers.append(member.center)
                current_age_groups.append(member.age_group)
        if db_field.name == 'session_name':
            approved_sessions = NewSession.objects.filter(approved=True)
            kwargs['queryset'] = approved_sessions.filter(center_name__in=current_centers, age_group__in=current_age_groups)

        if db_field.name == 'created_by':
            kwargs['queryset'] = User.objects.filter(pk=request.user.pk)

        if db_field.name == 'last_editted_by':
            kwargs['queryset'] = User.objects.filter(pk=request.user.pk)

        return super(ReportAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            return super(ReportAdmin, self).get_form(request, obj, **kwargs)

        if not profile.objects.filter(user=request.user).exists():
            return super(ReportAdmin, self).get_form(request, obj, **kwargs)

        current_profile = profile.objects.get(user=request.user)
        current_members = Membership.objects.filter(ymht=current_profile)
        role = Role.objects.get(role='Participant')
        active_roles = []
        for member in current_members:
            if member.is_active:
                active_roles.append(member.role.level)
        highest_level = max(active_roles)
        self.exclude = []
        if not (request.user.is_superuser or highest_level > 2):
            self.exclude.append('approved')
        return super(ReportAdmin, self).get_form(request, obj, **kwargs)

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})}
    }


class NewSessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'location', 'approved')
    search_fields = ('name', 'location')
    fields = ['name', 'center_name', 'age_group', 'description', 'event_type',
              'start_date', 'start_time', 'end_date', 'end_time', 'location',
              'sms_content', 'email_subject', 'email_body', 'approved']
              # 'created_by' is omitted because of an error
    def get_readonly_fields(self, request, obj=None):
        user_is_coord_of_current_center = False
        status = return_status(request, obj)
        result = {
                'Superuser': [],
                'Other User': self.readonly_fields + self.fields,
                'Center Coordinator': ['created_by'],
                'New Object': [],
            }[status]
        return result

    def queryset(self, request):
        qs = super(NewSessionAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs

        if not profile.objects.filter(user=request.user).exists():
            return NewSession.objects.none()
        current_profile = profile.objects.get(user=request.user)

        if not Membership.objects.filter(ymht=current_profile).exists():
            return NewSession.objects.none()

        current_members = Membership.objects.filter(ymht=current_profile)
        current_centers = []
        current_age_groups = []
        for member in current_members:
            if member.is_active:
                current_centers.append(member.center)
                current_age_groups.append(member.age_group)
        # Filtered the queryset twice based on age_group & center
        filtered_qs = qs.filter(center_name__in=current_centers)
        return filtered_qs.filter(age_group__in=current_age_groups)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            return super(NewSessionAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
# If profile for current user does not exist, then what to do?
        if not profile.objects.filter(user=request.user).exists():
            return super(NewSessionAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

        current_profile = profile.objects.get(user=request.user)
        current_members = Membership.objects.filter(ymht=current_profile)
        current_centers_pk = []
        current_age_group_pk = []
        for member in current_members:
            if member.is_active:
                # Only if helper or above then can add the center
                if member.role.level > PARTICIPANT_ROLE_LEVEL:
                    current_centers_pk.append(member.center.pk)
                    current_age_group_pk.append(member.age_group.pk)
        if db_field.name == 'center_name':
            kwargs['queryset'] = Center.objects.filter(pk__in=current_centers_pk)
        if db_field.name == 'age_group':
            kwargs['queryset'] = AgeGroup.objects.filter(pk__in=current_age_group_pk)
        return super(NewSessionAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if db_field.name == 'created_by':
            kwargs['queryset'] = request.user

        return super(NewSessionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            return super(NewSessionAdmin, self).get_form(request, obj, **kwargs)

        if not profile.objects.filter(user=request.user).exists():
            return super(NewSessionAdmin, self).get_form(request, obj, **kwargs)

        current_profile = profile.objects.get(user=request.user)
        current_members = Membership.objects.filter(ymht=current_profile)
        role = Role.objects.get(role='Participant')
        active_roles = []
        for member in current_members:
            if member.is_active:
                active_roles.append(member.role.level)
        highest_level = max(active_roles)
        self.exclude = []
        if not (request.user.is_superuser or highest_level > 2):
            self.exclude.append('approved')
        return super(NewSessionAdmin, self).get_form(request, obj, **kwargs)

admin.site.register(Report, ReportAdmin)
admin.site.register(NewSession, NewSessionAdmin)
