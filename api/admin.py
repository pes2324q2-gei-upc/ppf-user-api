"""
This document contains all the models that will be registered in the admin panel.
"""

from django.contrib import admin
from ppf.common.models.user import User, Driver

# Register your models here.

admin.site.register([User, Driver])
