from chat.models import ChatSession, ChatMessage
from repositories.models import RepoFile, FileChunk, ChunkEmbedding
from django.db.models import Q
from sentence_transformers import SentenceTransformer
import numpy as np
import openai
from django.conf import settings
from typing import Optional
import os

from chat.models import ChatSession, ChatMessage
from repositories.models import RepoFile, FileChunk, ChunkEmbedding
from django.db.models import Q
from sentence_transformers import SentenceTransformer
import numpy as np
import os

class ChatService:
    def __init__(self, model_path: str = "/app/bge-m3"):
        self.model = None
        self.model_path = model_path

        if not os.environ.get("CI"):
            try:
                self.model = SentenceTransformer(self.model_path)
            except Exception as e:
                print(f"Failed to load embedding model: {e}")
                self.model = None

    def embed_query(self, query: str):
        if self.model is None:
            raise RuntimeError("Embedding model is not available (likely running in CI).")
        return self.model.encode(query)

    def search_relevant_chunks(self, file: RepoFile, query: str, top_k: int = 5):
        if self.model is None:
            print("Skipping semantic search because model is unavailable (CI).")
            return []

        query_vector = self.embed_query(query)

        chunks = FileChunk.objects.filter(repo_file=file).select_related("chunkembedding")
        scored = []

        for chunk in chunks:
            try:
                embedding = np.array(chunk.chunkembedding.embedding)
                score = np.dot(embedding, query_vector) / (
                    np.linalg.norm(embedding) * np.linalg.norm(query_vector)
                )
                scored.append((score, chunk))
            except Exception:
                continue

        scored.sort(key=lambda x: x[0], reverse=True)
        return [chunk for _, chunk in scored[:top_k]]

    def answer_about_file(self, session: ChatSession, file: RepoFile, question: str) -> str:
        
        ChatMessage.objects.create(session=session, sender="user", message=question)

        
        top_chunks = self.search_relevant_chunks(file, question)
        context = "\n\n".join(chunk.content for chunk in top_chunks)

        
        prompt = f"""You are an assistant answering questions about a specific code file.
            The user asked:
            \"{question}\"

            Relevant code snippets:
            {context}

            Answer clearly and helpfully."""

        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            answer = response.choices[0].message.content.strip()
        except Exception as e:
            answer = f"(OpenAI error: {e})"

        ChatMessage.objects.create(session=session, sender="ai", message=answer)

        return answer
