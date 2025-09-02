from django.urls import path
from repositories.views.repo_views import FetchTreeView, FetchFileContentView

urlpatterns = [
    path("tree/", FetchTreeView.as_view()),
    path("content/<str:owner>/<str:repo>/<str:sha>/", FetchFileContentView.as_view()),
]