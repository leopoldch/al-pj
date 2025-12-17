from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound

from core.services import BucketPointService 

class BucketPointView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, _):
        data = BucketPointService.get_all()
        return Response(data)

    def post(self, request):
        try:
            data = BucketPointService.create(
                data=request.data, 
                context={"request": request}
            )
            return Response(data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            data = BucketPointService.update(pk=pk, data=request.data)
            return Response(data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except NotFound as e:
            return Response({"detail": str(e.detail)}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, _, pk):
        try:
            BucketPointService.delete(pk=pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except NotFound as e:
            return Response({"detail": str(e.detail)}, status=status.HTTP_404_NOT_FOUND)