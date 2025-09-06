from django.urls import path
from chat.views.file_chat_view import FileChatView

urlpatterns = [
    path("file/", FileChatView.as_view(), name="file-chat"),
]
