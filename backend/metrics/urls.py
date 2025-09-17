from django.urls import path
from .views import MetricsExtractionView
from .views import PredictRepoStabilityView

urlpatterns = [
    path("extract/<int:repo_id>/", MetricsExtractionView.as_view(), name="extract-metrics"),
    path("predict/<int:repo_id>/", PredictRepoStabilityView.as_view()),
]
