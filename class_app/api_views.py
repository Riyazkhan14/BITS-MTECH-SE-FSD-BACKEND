from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,authentication_classes

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .models import Classes

@api_view(['GET',])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated,))
def all_classes(request):
    classes = Classes.objects.filter(is_delete=False)
    classes_list = []
    for one in classes:
        classes_list.append({'pk':one.pk,'name':one.name,'created_at':one.created_at})
    response = {
                'status':200,
                'message': "success",
                'data':{'all_classes':classes_list}
            }
    return Response(response,status=status.HTTP_200_OK)
