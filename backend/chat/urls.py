from django.urls import path
from chat.views.file_chat_view import FileChatView
from chat.views.file_chat_view import CreateChatSessionView

urlpatterns = [
    path("file/", FileChatView.as_view(), name="file-chat"),
    path("sessions/", CreateChatSessionView.as_view(), name="create-chat-session"),
]
