import os
import sys
import csv

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MHT_Portal.settings")

from django.contrib.auth.models import User
from profile.models import profile, Membership
from masters.models import Hobby, Center, AgeGroup, Role, SubRole
import datetime

csvfile = open('profiles_left.csv', 'rb')
reader = csv.reader(csvfile,)
for row in reader:
    current_user = User.objects.get(username=row[0])
    try:
        prof = profile.objects.get(user=current_user)
    except:
        prof = profile()
        prof.user = User.objects.get(username=row[0])
    prof.first_name = row[1]
    prof.last_name = row[2]
    prof.date_of_birth = datetime.date.today()
    prof.save()
    prof.hobby = [Hobby.objects.get(id=1)]
    prof.father_name = "Please input"
    prof.mother_name = "Please input"
    prof.save()
    try:
        member = Membership.objects.get(ymht=prof)
    except:
        member = Membership()
        member.ymht = prof
    member.center = Center.objects.get(center_name=row[3])
    member.age_group = AgeGroup.objects.get(age_group=row[4])
    member.role = Role.objects.get(role=row[5])
#     member.sub_role = Subrole.objects.filter() # Add code to insert subroles 
    member.since = datetime.date.today()
    member.is_active = True
    member.save()
    if row[6]:
        member.sub_role.add(SubRole.objects.get(sub_role="PR"))
    if row[7]:
        member.sub_role.add(SubRole.objects.get(sub_role="Admin"))
    if row[8]:
        member.sub_role.add(SubRole.objects.get(sub_role="Academics"))
    if row[9]:
        member.sub_role.add(SubRole.objects.get(sub_role="Exec"))
    if row[10]:
        member.sub_role.add(SubRole.objects.get(sub_role="Events"))
#     if row[11]:
        # Check if row[11] is true and one of rows[6] to [10] are also true then add another membership object 
        # with role = Helper
