from django.urls import path
from map.views import map_views
from map.views.map_views import MapDataView

urlpatterns = [
    path("nodes/", map_views.NodePositionListCreateView.as_view(), name="node-position"),
    path("edges/", map_views.FileEdgeListCreateView.as_view(), name="file-edge"),
    path('data/<int:repo_id>/', MapDataView.as_view(), name='map-data'),
]
