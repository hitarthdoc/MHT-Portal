import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MHT_Portal.settings")
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
# import django.contrib.auth.modelsS
import csv

csvfile = open('users_left.csv', 'rb')
reader = csv.reader(csvfile,)
for row in reader:
    user = User.objects.create_user(row[0], row[1], row[2],)
    user.first_name = row[3]
    user.last_name = row[4]
    user.is_active = True
    user.is_staff = True
    user.groups = [Group.objects.get(name = row[5])]
    user.save()