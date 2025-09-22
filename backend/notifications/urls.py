# notifications/urls.py
from django.urls import path
from notifications.views.notification_views import (
    NotificationListCreateView,
    NotificationDetailView,
    MarkAsReadView,
    MarkAllAsReadView,
    DeleteNotificationView,
    WatchedReposSummaryView
)

urlpatterns = [
    path('', NotificationListCreateView.as_view(), name='notification-list-create'),
    path('<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),
    path('<int:pk>/mark-read/', MarkAsReadView.as_view(), name='notification-mark-read'),
    path('mark-all-read/', MarkAllAsReadView.as_view(), name='notification-mark-all-read'),
    path('<int:pk>/delete/', DeleteNotificationView.as_view(), name='notification-delete'),
    path("watched-repos-summary/", WatchedReposSummaryView.as_view()),
]
