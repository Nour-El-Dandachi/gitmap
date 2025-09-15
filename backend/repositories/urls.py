from django.urls import path
from repositories.views.repo_views import (
    FetchTreeView,
    FetchFileContentView,
    AddRepositoryView,
    UserRepositoriesView,
    UpdateLastShaView
)
from repositories.views.map_views import RepoFileImportsView
from repositories.views.map_ai_views import RepoMapAIView
from repositories.views.map_ai_views import ImportantFilesForMapView
from repositories.views.map_views import RepoMapView
from repositories.views.map_views import RepoMapExistsView


urlpatterns = [

    path('<int:repo_id>/map/', RepoMapView.as_view(), name='repo-code-map'),


    path("<int:repo_id>/important-files/", ImportantFilesForMapView.as_view(), name="important-files"),
    path("<int:repo_id>/map-ai/", RepoMapAIView.as_view(), name="repo-map-ai"),

    path("<int:repo_id>/exists/", RepoMapExistsView.as_view()),

   
    path("<int:repo_id>/file-imports/", RepoFileImportsView.as_view(), name="repo-file-imports"),

    
    path("tree/", FetchTreeView.as_view()),
    path("content/<str:owner>/<str:repo>/<str:sha>/", FetchFileContentView.as_view()),
    path("add/", AddRepositoryView.as_view(), name="add-repo"),
    path("update-sha/", UpdateLastShaView.as_view(), name="update-sha"),
    path("user/", UserRepositoriesView.as_view(), name="user-repositories"),
]
