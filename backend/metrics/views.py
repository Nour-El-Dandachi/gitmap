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


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response


class PredictRepoStabilityView(APIView):
    @swagger_auto_schema(
        operation_summary="Predict defects for repository files",
        operation_description="Run the ML model on repository metrics and return predictions for each file. Requires Bearer token authentication.",
        manual_parameters=[
            openapi.Parameter(
                "repo_id",
                openapi.IN_PATH,
                description="Repository ID",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
        ],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "repo_id": openapi.Schema(type=openapi.TYPE_INTEGER, example=13),
                    "count": openapi.Schema(type=openapi.TYPE_INTEGER, example=21),
                    "results": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "filemetrics_id": openapi.Schema(type=openapi.TYPE_INTEGER, example=73),
                                "repo_file_id": openapi.Schema(type=openapi.TYPE_INTEGER, example=651),
                                "pred": openapi.Schema(type=openapi.TYPE_STRING, example="false"),
                                "p_true": openapi.Schema(type=openapi.TYPE_NUMBER, example=0.22),
                                "p_false": openapi.Schema(type=openapi.TYPE_NUMBER, example=0.78),
                            },
                        ),
                    ),
                },
            ),
            404: openapi.Response("No metrics found for this repo."),
        },
    )
    def post(self, request, repo_id: int):
        results = predict_repo(repo_id)
        if not results:
            return Response({"error": "No metrics found for this repo."}, status=404)
        return Response({
            "repo_id": repo_id,
            "count": len(results),
            "results": results
        })
