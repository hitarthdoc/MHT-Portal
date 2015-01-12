import os

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MHT_Portal.settings")

from profile.models import profile, Membership
import datetime
from masters.models import Center, City

def centres_to_add(centre_name):
#     returns List of centres to be added
    if centre_name == "Dombivali":
        return ["Borivali", "Ghatkopar", "Ville Parle"]
    if centre_name == "Borivali":
        return ["Dombivali", "Ghatkopar", "Ville Parle"]
    if centre_name == "Ghatkopar":
        return ["Dombivali", "Borivali", "Ville Parle"]
    if centre_name == "Ville Parle":
        return ["Dombivali", "Borivali", "Ghatkopar"]
    
    return
center_name_list = ["Dombivali", "Borivali", "Ghatkopar", "Ville Parle"]
Mumbai = City.objects.get(name="Mumbai")
Mumbai_centres = Center.objects.filter(city=Mumbai)
Mumbai_members = Membership.objects.filter(center__in=Mumbai_centres)
for member in Mumbai_members:
    prof = member.ymht # Profile
    current_center = member.center
    centre_name = current_center.center_name
    to_add_centers = centres_to_add(centre_name)
    for center in to_add_centers:
        member = Membership()
        member.ymht = prof
        member.center = Center.objects.get(center_name=center)
# profile.objects.filter()