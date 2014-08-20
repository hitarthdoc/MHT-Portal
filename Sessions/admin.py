from operator import __or__ as OR
from django.contrib import admin
from django.db import models
from django.forms import TextInput, Textarea
from .models import *
from profile.models import Membership, Profile, Center, Role


class SessionFlowInline(admin.TabularInline):
	model = SessionFlow
	extra = 1
	formfield_overrides = {
		models.CharField: {'widget': TextInput(attrs={'size':'20'})},
		models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
	}

	def get_readonly_fields(self, request, obj=None):
		if obj:
			if obj.approved == True:
				return ('session', 'time', 'activity', 'description', 'details')
			else:
				return []
		else:
			return []

class SessionMediaInline(admin.TabularInline):
	model = SessionMedia

	extra = 1

	def get_readonly_fields(self, request, obj=None):
		if obj:
			if obj.approved == True:
				return ('session', 'title', 'category', 'attachment')
			else:
				return []
		else:
			return []


class AttendanceInline(admin.TabularInline):
	model = Attendance
	filter_horizontal = ("ymht",)
	extra = 1
	max_num = 1
	can_delete = False

	# def get_readonly_fields(self, request, obj=None):
	# 	if obj:
	# 		if obj.approved == True:
	# 			return ('ymht', 'session')
	# 		else:
	# 			return []
	# 	else:
	# 		return []

	
	def formfield_for_manytomany(self, db_field, request, **kwargs):
		if not Profile.objects.filter(user=request.user).exists():
			if db_field.name == 'ymht':
				participant_or_helper = Role.objects.filter(level__lt=3)
				part_members = Membership.objects.filter(role = participant_or_helper)
				kwargs['queryset'] = part_members
			return super(AttendanceInline, self).formfield_for_manytomany(db_field, request, **kwargs)

		current_profile = Profile.objects.get(user=request.user)
		current_members = Membership.objects.filter(ymht=current_profile)
		current_centers = []
		current_age_groups = []
		for member in current_members:
			if member.is_active:
				current_centers.append(member.center)
				current_age_groups.append(member.age_group)

		if db_field.name == 'ymht':
			participant_or_helper = Role.objects.filter(level__lt=3)
			part_members = Membership.objects.filter(role = participant_or_helper)
			part_members = part_members.filter(center__in=current_centers, age_group__in=current_age_groups)
			participant_profiles = Profile.objects.filter(membership__in=part_members)
			kwargs['queryset'] = participant_profiles.distinct()
		return super(AttendanceInline, self).formfield_for_manytomany(db_field, request, **kwargs)

class CoordAttendanceInline(admin.TabularInline):
	model = CoordinatorsAttendance
	filter_horizontal = ("coords",)
	max_num = 1
	extra = 1
	can_delete = False

	# def get_readonly_fields(self, request, obj=None):
	# 	if obj:
	# 		if obj.approved == True:
	# 			return ('coords', 'session')
	# 		else:
	# 			return []
	# 	else:
	# 		return []

	def formfield_for_manytomany(self, db_field, request, **kwargs):
		if not Profile.objects.filter(user=request.user).exists():
			if db_field.name == 'coords':
				coordinator = Role.objects.get(role='Coordinator')
				coords_members = Membership.objects.filter(role = coordinator)
				kwargs['queryset'] = coords_members
			return super(CoordAttendanceInline, self).formfield_for_manytomany(db_field, request, **kwargs)

		current_profile = Profile.objects.get(user=request.user)
		current_members = Membership.objects.filter(ymht=current_profile)
		current_centers = []
		current_age_groups = []
		for member in current_members:
			if member.is_active:
				current_centers.append(member.center)
				current_age_groups.append(member.age_group)

		if db_field.name == 'coords':
			coordinator = Role.objects.get(role='Coordinator')
			coords_members = Membership.objects.filter(role = coordinator)
			coords_members = coords_members.filter(center__in=current_centers, age_group__in=current_age_groups)
			coords_profiles = Profile.objects.filter(membership__in=coords_members)
			kwargs['queryset'] = coords_profiles.distinct()
		return super(CoordAttendanceInline, self).formfield_for_manytomany(db_field, request, **kwargs)

class ReportAdmin(admin.ModelAdmin):
	inlines = [
		SessionFlowInline,
		SessionMediaInline,
		AttendanceInline,
		CoordAttendanceInline,
	]
	
	list_display = ('session_name', 'created_by', 'approved')
	
	def get_readonly_fields(self, request, obj=None):
		if obj:
			if obj.approved == True:
				return ('session_name', 'date', 'place', 'Duration', 'improvement', 'category', 'attachment', 'created_by')
			else:
				return []
		else:
			return []

	def queryset(self, request):
		qs = super(ReportAdmin, self).queryset(request)
		if request.user.is_superuser:
			return qs

		approved_qs = qs.filter(approved=True)
		if not Profile.objects.filter(user=request.user).exists():
			return Report.objects.none()
		
		current_profile = Profile.objects.get(user=request.user)
		if not Membership.objects.filter(ymht=current_profile).exists():
			return Report.objects.none()

		current_members = Membership.objects.filter(ymht=current_profile)
		current_centers = []
		current_age_groups = []
		current_roles = []
		for member in current_members:
			if member.is_active:
				current_centers.append(member.center)
				current_age_groups.append(member.age_group)
				current_roles.append(member.role.level)

		filtered_qs = qs.filter(session_name__center_name__in=current_centers)
		filtered_qs = filtered_qs.filter(session_name__age_group__in=current_age_groups)
		if max(current_roles) > 2:
			approved_qs = reduce(OR, [approved_qs, filtered_qs])
			print str(approved_qs)
		return approved_qs


	def formfield_for_manytomany(self, db_field, request, **kwargs):
		if request.user.is_superuser:
			return super(ReportAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
# If Profile for current user does not exist, then what to do?
		if not Profile.objects.filter(user=request.user).exists():
			return super(ReportAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

		current_profile = Profile.objects.get(user=request.user)
		current_members = Membership.objects.filter(ymht=current_profile)
		current_centers_pk = []
	#   current_age_group_pk = []
		for member in current_members:
			if member.is_active:
				current_centers_pk.append(member.center.pk)
			#   current_age_group_pk.append(member.age_group.pk)    
		if db_field.name == 'center_name':
			kwargs['queryset'] = Center.objects.filter(pk__in=current_centers_pk)
	#   if db_field.name == 'age_group':
	#       kwargs['queryset'] = AgeGroup.objects.filter(pk__in=current_age_group_pk)
		return super(ReportAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if request.user.is_superuser:
			return super(ReportAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
		if not Profile.objects.filter(user=request.user).exists():
			return super(ReportAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

		current_profile = Profile.objects.get(user=request.user)
		current_members = Membership.objects.filter(ymht=current_profile)
		current_centers = []
		for member in current_members:
			if member.is_active:
				current_centers.append(member.center)    
		if db_field.name == 'session_name':
			temp = NewSession.objects.filter(approved=True)
			kwargs['queryset'] = temp.filter(center_name__in=current_centers)

		if db_field.name == 'created_by':
			kwargs['queryset'] = User.objects.filter(pk=request.user.pk)

		return super(ReportAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


	def get_form(self, request, obj=None, **kwargs):
		if request.user.is_superuser:
			return super(ReportAdmin, self).get_form(request, obj, **kwargs)

		if not Profile.objects.filter(user=request.user).exists():
			return super(ReportAdmin, self).get_form(request, obj, **kwargs)

		current_profile = Profile.objects.get(user=request.user)
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
		models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})}
	}

class NewSessionAdmin(admin.ModelAdmin):
	list_display = ('name', 'start_date', 'approved')
	def queryset(self, request):
		qs = super(NewSessionAdmin, self).queryset(request)
		if request.user.is_superuser:
			return qs

		if not Profile.objects.filter(user=request.user).exists():
			return NewSession.objects.none()
		current_profile = Profile.objects.get(user=request.user)
		
		if not Membership.objects.filter(ymht=current_profile).exists():
			return NewSession.objects.none()
		
		current_members = Membership.objects.filter(ymht=current_profile)
		current_centers = []
		current_age_groups = []
		for member in current_members:
			if member.is_active:
				current_centers.append(member.center)
				current_age_groups.append(member.age_group)
		#Filtered the queryset twice based on age_group & center
		filtered_qs = qs.filter(center_name__in=current_centers)
		return filtered_qs.filter(age_group__in=current_age_groups)
		
	def formfield_for_manytomany(self, db_field, request, **kwargs):
		if request.user.is_superuser:
			return super(NewSessionAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
# If Profile for current user does not exist, then what to do?
		if not Profile.objects.filter(user=request.user).exists():
			return super(NewSessionAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

		current_profile = Profile.objects.get(user=request.user)
		current_members = Membership.objects.filter(ymht=current_profile)
		current_centers_pk = []
		current_age_group_pk = []
		for member in current_members:
			if member.is_active:
# Only if helper or above then can add the center
				if member.role.level > 1:
					current_centers_pk.append(member.center.pk)
					current_age_group_pk.append(member.age_group.pk)	
		if db_field.name == 'center_name':
			kwargs['queryset'] = Center.objects.filter(pk__in=current_centers_pk)
		if db_field.name == 'age_group':
			kwargs['queryset'] = AgeGroup.objects.filter(pk__in=current_age_group_pk)
		return super(NewSessionAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if request.user.is_superuser:
			return super(NewSessionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


		if db_field.name == 'created_by':
			kwargs['queryset'] = User.objects.filter(pk=request.user.pk)

		return super(NewSessionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

	#for approval

	def get_form(self, request, obj=None, **kwargs):
		if request.user.is_superuser:
			return super(NewSessionAdmin, self).get_form(request, obj, **kwargs)

		if not Profile.objects.filter(user=request.user).exists():
			return super(NewSessionAdmin, self).get_form(request, obj, **kwargs)

		current_profile = Profile.objects.get(user=request.user)
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
