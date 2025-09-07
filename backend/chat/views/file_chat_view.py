from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from chat.models import ChatSession
from repositories.models import RepoFile
from chat.services.chat_service import ChatService
from utils.response import responseJSON

chat_service = ChatService(model_path="/app/bge-m3")

class FileChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        session_id = request.data.get("session_id")
        file_id = request.data.get("file_id")
        question = request.data.get("question")

        if not all([session_id, file_id, question]):
            return responseJSON({"error": "Missing required fields."}, status="error", status_code=400)

        try:
            session = ChatSession.objects.get(id=session_id, user=request.user)
            file = RepoFile.objects.get(id=file_id)

            answer = chat_service.answer_about_file(session, file, question)

            return responseJSON({"answer": answer}, status="success", status_code=200)

        except ChatSession.DoesNotExist:
            return responseJSON({"error": "Invalid chat session."}, status="error", status_code=404)

        except RepoFile.DoesNotExist:
            return responseJSON({"error": "File not found."}, status="error", status_code=404)

        except Exception as e:
            return responseJSON({"error": str(e)}, status="error", status_code=500)
