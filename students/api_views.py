from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,authentication_classes

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from class_app.models import Classes
from drives.models import Vaccine_Drives
from .models import Student

import csv

@api_view(['GET',])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated,))
def all_students(request):
    students = Student.objects.filter(is_delete=False)
    student_list = []
    for one in students:
        student_list.append({'pk':one.pk,'name':one.name,'student_id':one.student_id,'Class_id':one.Class_id.pk,'class_name':one.Class_id.name,'created_at':one.created_at})
    response = {
                'status':200,
                'message': "success",
                'data':{'student_list':student_list}
            }
    return Response(response,status=status.HTTP_200_OK)


@api_view(['POST',])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated,))
def add_student(request):
    if request.method == "POST":
        class_obj = Classes.objects.get(pk=int(request.POST['class_id']))
        if not Student.objects.filter(name=request.POST['name'],Class_id=class_obj,is_delete=False).exists():
            one = Student.objects.create(name=request.POST['name'],
                                         Class_id=class_obj,
                                         student_id = request.POST['student_id'])
            response = {
                    'status':200,
                    'message': "success",
                    'data':{'message':"Student added Successfully",
                    'student':{'pk':one.pk,'name':one.name,'Class_id':one.Class_id.pk,'class_name':one.Class_id.name,'student_id':one.student_id,'created_at':one.created_at}}
                }
            return Response(response,status=status.HTTP_200_OK)
        else:
            response = {
                    'status':400,
                    'message': "failed",
                    'data':{'message':"Student Already Exists !"}
                }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST',])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated,))
def update_student(request,pk):
    student_obj = Student.objects.get(pk=pk)
    if request.method == "POST":
        student_obj.student_id = request.POST['student_id']
        class_obj = Classes.objects.get(pk=int(request.POST['class_id']))
        if not Student.objects.filter(name=request.POST['name'],Class_id=class_obj,is_delete=False).exclude(pk=pk).exists():
            student_obj.name = request.POST['name']
            student_obj.Class_id=class_obj
        student_obj.save()
        response = {
            'status':200,
            'message': "success",
            'data':{'message':"Student Updated Successfully",'student':{'pk':student_obj.pk,'name':student_obj.name,'Class_id':student_obj.Class_id.pk,'class_name':student_obj.Class_id.name,'student_id':student_obj.student_id,'created_at':student_obj.created_at}}
        }
    return Response(response,status=status.HTTP_200_OK)


@api_view(['GET',])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated,))
def delete_student(request,pk):
    student_obj = Student.objects.get(pk=pk)
    student_obj.is_delete = True
    student_obj.save()
    response = {
            'status':200,
            'message': "success",
            'data':{'message':"Student Deleted Successfully"}
        }
    return Response(response,status=status.HTTP_200_OK)

@api_view(['POST',])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated,))
def student_upload(request):
    if request.method == "POST":
        import_file = request.FILES['import_file']
        ext = import_file.name.split(".")[-1]
        if ext == "csv":
            row_data = []
            unupload_data = []
            decoded_file = import_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            i = 0
            for row in reader:
                if Classes.objects.filter(pk=int(row['class_id'])).exists():
                    class_obj = Classes.objects.get(pk=int(row['class_id']))
                    if not Student.objects.filter(name=row['name'],Class_id=class_obj,is_delete=False).exists():
                        one = Student.objects.create(name=row['name'],
                                             Class_id=class_obj,
                                             student_id = row['student_id'])
                    else:
                        i = i + 1
                        unupload_data.append({'student_id':row['student_id'],'name':row['name'],'class_id':row['class_id'],'reason':'Student Already exists !'})
                else:
                    i = i + 1
                    unupload_data.append({'student_id':row['student_id'],'name':row['name'],'class_id':row['class_id'],'reason':"Class id doesn't Already exists !"})
            if len(unupload_data) == 0:
                response = {
                        'status':200,
                        'message': "success",
                        'data':{'message':"Data uploaded Successfully"}
                    }
                return Response(response,status=status.HTTP_200_OK)
            else:
                response = {
                        'status':200,
                        'message': "success",
                        'data':{'unupload_data':unupload_data}
                    }
                return Response(response,status=status.HTTP_200_OK)

        else:
            response = {
                    'status':400,
                    'message': "failed",
                    'data':{'message':"File Type must be CSV !"}
                }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)
