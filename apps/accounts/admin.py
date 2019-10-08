# encoding: utf-8
from django.contrib import admin
from apps.accounts.models import *


class ProfileAdminInline(admin.StackedInline):
    model = Profile
    can_delete = False


class ProfileRegistrationAdminInline(admin.StackedInline):
    model = ProfileRegistration
    can_delete = False
