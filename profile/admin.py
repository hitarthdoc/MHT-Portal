from django import forms
from django.contrib import admin
from django_countries.fields import CountryField
from masters.models import Role, Center
from profile.models import Profile, Membership
from profile.models import YMHTMobile, YMHTEmail
from profile.models import YMHTAddress, YMHTEducation
from profile.models import YMHTJob, GNCSewaDetails
from profile.models import LocalEventSewaDetails, GlobalEventSewaDetails
from Sessions.models import NewSession, Report
from Sessions.models import SessionFlow, SessionMedia
from Sessions.models import Attendance, CoordinatorsAttendance
from constants import PARTICIPANT_ROLE_LEVEL


class YMHTMobileInline(admin.StackedInline):
    model = YMHTMobile
    extra = 1


class YMHTEmailInline(admin.StackedInline):
    model = YMHTEmail
    extra = 1


class YMHTAddressInline(admin.StackedInline):
    model = YMHTAddress
    extra = 1


class YMHTEducationInline(admin.StackedInline):
    model = YMHTEducation
    extra = 1


class YMHTJobInline(admin.StackedInline):
    model = YMHTJob
    extra = 1


class RequiredFormSet(forms.models.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)
        self.forms[0].empty_permitted = False


class YMHTMembershipInline(admin.StackedInline):
    # fields = ('profile' , 'center' , 'age_group' , 'role', 'since', 'till', 'is_active')
    list_display = ('center')
    model = Membership
    formset = RequiredFormSet
    extra = 1

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if request.user.is_superuser or not profile.objects.filter(user=request.user).exists():
                return self.readonly_fields 

            current_profile = profile.objects.get(user=request.user)

            if not Membership.objects.filter(profile=current_profile).exists():
                return self.readonly_fields 

            current_membership = Membership.objects.filter(profile=current_profile)

            current_roles = []

            for member in current_membership:
                if member.is_active:
                    current_roles.append(member.role.level)

            highest_level = max(current_roles)

            current_obj_members = Membership.objects.filter(profile=obj)

            current_obj_roles = []

            for member in current_obj_members:

                if member.is_active:
                    current_obj_roles.append(member.role.level)

            highest_obj_level = max(current_obj_roles)
            if (highest_obj_level >= highest_level):
                self.extra = 0
                self.max_num = 0
                self.can_delete = False
                return self.readonly_fields + ('center', 'age_group', 'role',
                                               'sub_role', 'since', 'till', 'is_active')
            else:
                return []
        else:
            return self.readonly_fields 

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            return super(YMHTMembershipInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

        if not profile.objects.filter(user=request.user).exists():
            return super(YMHTMembershipInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

        current_profile = profile.objects.get(user=request.user)
        current_members = Membership.objects.filter(profile=current_profile)
        current_centers_pk = []
        current_age_group_pk = []
        current_roles = []
        for member in current_members:
            if member.is_active:
                current_centers_pk.append(member.center.pk)
                current_age_group_pk.append(member.age_group.pk)
                current_roles.append(member.role.level)

        if db_field.name == 'center':
            kwargs['queryset'] = Center.objects.filter(pk__in=current_centers_pk)
        if db_field.name == 'age_group':
            kwargs['queryset'] = AgeGroup.objects.filter(pk__in=current_age_group_pk)
        if db_field.name == 'role':
            try:
                kwargs['queryset'] = Role.objects.filter(level__lt=max(current_roles))
            except:
                kwargs['queryset'] = Role.objects.none()
        return super(YMHTMembershipInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_formset(self, request, obj=None, **kwargs):
        self.exclude = []
        if not request.user.is_superuser:
            self.exclude.append('sub_role')
        return super(YMHTMembershipInline, self).get_formset(request, obj, **kwargs)

    # TODO: Fetch subrole fields based on selection in role

    # def queryset(self, request):
    # qs = super(YMHTMembershipInline, self).queryset(request)
    #     if request.user.is_superuser:
    #         return qs

    #     if not profile.objects.filter(user=request.user).exists():
    #         return Membership.objects.none()
    #     current_profile = profile.objects.get(user=request.user)

    #     if not Membership.objects.filter(ymht=current_profile, is_active=True).exists():
    #         return Membership.objects.none()

    #     current_members = Membership.objects.filter(ymht=current_profile)
    #     current_centers = []
    #     current_age_groups = []
    #     current_roles = []

    #     for member in current_members:
    #         if member.is_active:
    #             current_roles.append(member.role.level)
    #             current_centers.append(member.center)
    #             current_age_groups.append(member.age_group)
    #     level_filtered_qs = qs.filter(role__level__lt=max(current_roles))
    #     return level_filtered_qs.filter(center__in=current_centers, age_group__in=current_age_groups)


# TODO: Known issue: In case of a MHT with multiple memberships, e.g. earlier
# was in Borivali say from 2013 - 14, and then shifted to S. City. Then both the
# coordinators should be able to view his info. But, on opening the profile, the
# other centers membership should appear as read-only. Otherwise, if kept
# editable then the profile cannot be saved because the drop down for the
# Borivali coordinator has been filtered to show only Borivali in the centre
# options, and that would change the MHT's details, which we don't want.


class GlobalEventSewaDetailsInline(admin.TabularInline):
    model = GlobalEventSewaDetails
    extra = 1


class LocalEventSewaDetailsInline(admin.StackedInline):
    # fields = ('event', 'ymht' , 'coordinator', 'attended' , 'attended_days' , 'comments')
    model = LocalEventSewaDetails
    extra = 1


class GNCSewaDetailsInline(admin.StackedInline):
    # fields = ('event', 'ymht' , 'coordinator', 'attended' , 'attended_days' , 'comments')
    model = GNCSewaDetails
    extra = 1


class profileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'role',
                    'center_name')
    list_filter = ('first_name', 'hobby')
    search_fields = ('first_name', 'last_name',)
    inlines = [
        YMHTMobileInline,
        YMHTEmailInline,
        YMHTAddressInline,
        YMHTEducationInline,
        YMHTJobInline,
        YMHTMembershipInline,
        GlobalEventSewaDetailsInline,
        LocalEventSewaDetailsInline,
        GNCSewaDetailsInline,
    ]

    # TODO: Right now, in User, all the usernames list comes. But in future we should filter this down.
    #     How to do this is a good question. Ideas would be appreciated

    def role(self, obj):
        current_profile = obj
        if not Membership.objects.filter(profile=current_profile, is_active=True).exists():
            return " "
        current_members = Membership.objects.filter(profile=current_profile, is_active=True)
        max_role_level = 0
        for member in current_members:
            if member.is_active:
                role = member.role
                if role.level > max_role_level:
                    max_role_level = role.level
        if max_role_level == 0:
            return " "
        return Role.objects.get(level=max_role_level)

    role.short_description = 'Role'
    role.admin_order_field = 'membership__role__role'

    def center_name(self, obj):
        current_profile = obj
        if not Membership.objects.filter(profile=current_profile, is_active=True).exists():
            return " "

        current_members = Membership.objects.filter(profile=current_profile, is_active=True)
        count = 0
        current_centers = ""
        for member in current_members:
            if member.is_active:
                center = member.center
                count += 1
                current_centers += "(%s) %s, %s " % (count, center.center_name, center.city.name)
        return current_centers

    center_name.admin_order_field = 'membership__center__center_name'

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = []
        if not request.user.is_superuser:
            self.exclude.append('user')
        return super(profileAdmin, self).get_form(request, obj, **kwargs)

    def queryset(self, request):
        qs = super(profileAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs

        if not profile.objects.filter(user=request.user).exists():
            return profile.objects.none()
        current_profile = profile.objects.get(user=request.user)

        if not Membership.objects.filter(profile=current_profile, is_active=True).exists():
            return current_profile

        current_members = Membership.objects.filter(profile=current_profile, is_active=True)
        current_centers = []
        current_age_groups = []
        current_roles = []
        for member in current_members:
            if member.is_active:
                current_roles.append(member.role.level)
                current_centers.append(member.center)
                current_age_groups.append(member.age_group)
        for i, item in enumerate(current_roles):
            if current_roles[i] > PARTICIPANT_ROLE_LEVEL:
                memberships = Membership.objects.filter(
                    center=current_centers[i],
                    age_group=current_age_groups[i],
                    role__level__lte=current_roles[i])
        qs = qs.filter(membership__in=memberships)
        return qs.distinct()

    def get_formsets(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            yield inline.get_formset(request, obj)


admin.site.register(Profile, profileAdmin)
