from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ml_experiments.inference import predict_repo
from metrics.tasks import extract_metrics_for_repository

class MetricsExtractionView(APIView):
    def post(self, request, repo_id):
        extract_metrics_for_repository.delay(repo_id)
        return Response(
            {"message": f"Metrics extraction started for repo {repo_id}"},
            status=status.HTTP_202_ACCEPTED
        )


class PredictRepoStabilityView(APIView):
    def post(self, request, repo_id: int):
        results = predict_repo(repo_id)
        if not results:
            return Response({"error": "No metrics found for this repo."}, status=404)
        return Response({"repo_id": repo_id, "count": len(results), "results": results})
