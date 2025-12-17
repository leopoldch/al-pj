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
        data = BucketPointService.create(
            data=request.data, 
            context={"request": request}
        )
        return Response(data, status=status.HTTP_201_CREATED)


    def put(self, request, pk):
        data = BucketPointService.update(pk=pk, data=request.data)
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, _, pk):
        BucketPointService.delete(pk=pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
