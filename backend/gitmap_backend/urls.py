"""
URL configuration for gitmap_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from users.views.github_views import github_redirect, github_callback

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('auth/github/redirect/', github_redirect),
    path('auth/github/callback/', github_callback, name='github_callback'),
    
    path('api/users/', include('users.urls')),
    path("api/repos/", include("repositories.urls")),
    
    path("api/notifications/", include("notifications.urls")),
    path("api/chat/", include("chat.urls")),

    path('api/map/', include('map.urls')),
]
