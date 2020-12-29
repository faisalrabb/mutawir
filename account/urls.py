from django.urls import path, include
from accounts import views

url_pattern = [
    path('password/reset/', views.profile), #banned all auth operation
    path('password/set/', views.profile), #banned all auth operation
    path('password/change/', views.profile), #banned all auth operation
    path('profile/<slug:username>/', views.profile, name="user_profile"),
    path('profile/', views.profile, name="profile"),
    path('profile_info/', views.user_info, name="profile_info")
]
