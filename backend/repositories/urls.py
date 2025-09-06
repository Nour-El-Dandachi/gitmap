from django.urls import path
from repositories.views.repo_views import (
    FetchTreeView,
    FetchFileContentView,
    AddRepositoryView
)


urlpatterns = [
    path("tree/", FetchTreeView.as_view()),
    path("content/<str:owner>/<str:repo>/<str:sha>/", FetchFileContentView.as_view()),
    path('add/', AddRepositoryView.as_view(), name='add-repo'),
]