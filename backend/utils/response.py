from rest_framework.response import Response

def responseJSON(payload=None, status="success", status_code=200):
    return Response({
        "status": status,
        "payload": payload
    }, status=status_code)
