from django.urls import path
from map.views import map_views

urlpatterns = [
    path("nodes/", map_views.NodePositionListCreateView.as_view(), name="node-position"),
    path("edges/", map_views.FileEdgeListCreateView.as_view(), name="file-edge"),
]
