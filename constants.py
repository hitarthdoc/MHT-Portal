import datetime
from django.core.validators import RegexValidator

# Used in Sessions/admin
def return_status(request, obj=None):
    if request.user.is_superuser:
        return "Superuser"
    if obj:
        if (obj.approved is True) and (request.user != obj.created_by):
            return "Other User"
        else:
            return "Center Coordinator"
    else:
        return "New Object"


# Used in Sessions/admin
def global_get_readonly_fields(caller, request, obj=None):
    user_is_coord_of_current_center = False
    status = return_status(request, obj)
    result = {
            'Superuser': [],
            'Other User': caller.readonly_fields + caller.fields,
            'Center Coordinator': [],
            'New Object': [],
        }[status]
    return result

#function to return path for the porfile picture
def profile_picture_file_name(instance, filename):
  try:
    return '/'.join(['profile', instance.user.username, filename])
  except:
    return '/'.join(['profile', 'YMHTians', filename])

# Currently not used in Profile events but kept as reference 
EVENT_CATEGORY_CHOICES = ((0, 'GNC Day'),
                          (1, 'Summer Camp'),
                          (2, 'YUVA Camp'),
                          (3, 'Aptaputra Satsang'),
                          (4, 'General Satsang'),
                          (5, 'Parayan'),
                          (6, 'Janma Jayanti'),
                          (7, 'Picnic'))


YEAR_CHOICES = []
for r in range(1980, (datetime.datetime.now().year+1)):
    YEAR_CHOICES.append((r,r))

GENDER_CHOICES = (('male', "Male"),
              ('female', "Female"))

EDU_CHOICES = (('school', "School"),
               ('college', "College"))

ATTENDED_DETAILS = ((1, 'All Days'), (2, 'Partial Days'))

PARTICIPANT_ROLE_LEVEL = 1
HELPER_ROLE_LEVEL = 2
COORD_ROLE_LEVEL = 3

#Validators for the charfield
ONLY_DIGITS_VALIDATOR = [RegexValidator(
    r'^[0-9]*$', 'Only Digits Please!')]

ONLY_LETTERS_VALIDATOR = [RegexValidator(
    r'^[a-zA-Z]*$', 'Only Letters Please!')]
