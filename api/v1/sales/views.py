from sales.models import Sale
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.v1.sales.serializers import SaleSerializer
from rest_framework import status


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def sales(request):
    instances = Sale.objects.filter(is_deleted=False)
    serialized = SaleSerializer(instances, many=True, context={'request': request})

    response_data = {
        'StatusCode': 6000,
        'data': serialized.data
    }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def sale(request, pk):
    instance = None
    if Sale.objects.filter(is_deleted=False, pk=pk).exists():
        instance = Sale.objects.get(is_deleted=False, pk=pk)

    if instance:
        serialized = SaleSerializer(instance, context={'request': request})

        response_data = {
            'StatusCode': 6000,
            'data': serialized.data
        }
    else:
        response_data = {
            'StatusCode': 6001,
            'message': 'Sale not found.'
        }
    return Response(response_data, status=status.HTTP_200_OK)