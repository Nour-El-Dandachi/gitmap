from django.urls import path
from repositories.views.repo_views import (
    FetchTreeView,
    FetchFileContentView,
    AddRepositoryView,
    UserRepositoriesView
)
from repositories.views.repo_views import UpdateLastShaView
from repositories.views.map_views import RepoMapPreviewView


urlpatterns = [
    path('<int:repo_id>/map-preview/', RepoMapPreviewView.as_view(), name='repo-map-preview'),

    path("tree/", FetchTreeView.as_view()),
    path("content/<str:owner>/<str:repo>/<str:sha>/", FetchFileContentView.as_view()),
    path('add/', AddRepositoryView.as_view(), name='add-repo'),
    path("update-sha/", UpdateLastShaView.as_view(), name="update-sha"),
    path("user/", UserRepositoriesView.as_view(), name="user-repositories"),
]