"""
This file is used to define the URL patterns for the contact app.
"""

from django.urls import path
from achievement import views

urlpatterns = [
    path(
        "users/<int:id>/achievements/",
        views.UserAchievementList.as_view(),
        name="userAchievementList",
    ),
]
