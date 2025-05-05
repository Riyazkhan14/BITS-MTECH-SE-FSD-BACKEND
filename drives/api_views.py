from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse

from class_app.models import Classes
from .models import Vaccine_Drives,Students_Vaccination
from students.models import Student

import csv
from datetime import datetime,date
import xlwt
from django.db.models import Sum,Count

@api_view(['GET',])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated,))
def all_drives(request):
    drives = Vaccine_Drives.objects.filter(is_active=True,is_delete=False)
    drive_list = []
    for one in drives:
        drive_list.append({'pk':one.pk,'name':one.vaccine_name,'Class_id':one.Class_id.pk,'class_name':one.Class_id.name,'drive_date':one.drive_date,'available_slots':one.available_slots,'created_at':one.created_at})
    response = {
                'status':200,
                'message': "success",
                'data':{'drive_list':drive_list}
            }
    return Response(response,status=status.HTTP_200_OK)


# @api_view(['POST',])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated,))
# def add_drive(request):
#     if request.method == "POST":
#         class_obj = Classes.objects.get(pk=int(request.POST['class_id']))
#         if not Vaccine_Drives.objects.filter(vaccine_name=request.POST['vaccine_name'],Class_id=class_obj,is_active=True,is_delete=False).exists():
#             one = Vaccine_Drives.objects.create(vaccine_name=request.POST['vaccine_name'],
#                                          Class_id=class_obj,
#                                          drive_date = request.POST['drive_date'],
#                                          available_slots = int(request.POST['available_slots']),
#                                          is_active=True,
#                                          is_delete=False)
#             response = {
#                     'status':200,
#                     'message': "success",
#                     'data':{'message':"Drive added Successfully",'drive':{'pk':one.pk,'name':one.vaccine_name,'Class_id':one.Class_id.pk,'class_name':one.Class_id.name,'drive_date':one.drive_date,'available_slots':one.available_slots,'created_at':one.created_at}}
#                 }
#             return Response(response,status=status.HTTP_200_OK)
#         else:
#             response = {
#                     'status':400,
#                     'message': "failed",
#                     'data':{'message':"Drive Already Exists !"}
#                 }
#             return Response(response,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST',])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated,))
def add_drive(request):
    if request.method == "POST":
        class_obj = Classes.objects.get(pk=int(request.POST['class_id']))
        if not Vaccine_Drives.objects.filter(vaccine_name=request['vaccine_name'],Class_id=class_obj,is_active=True,is_delete=False).exists():
            drive_date = datetime.strptime(request.POST['drive_date'],'%Y-%m-%d')
            delta = drive_date - date.today()
            if delta.days >= 15:
                one = Vaccine_Drives.objects.create(vaccine_name=request['vaccine_name'],
                                            Class_id=class_obj,
                                            drive_date = request.POST['drive_date'],
                                            available_slots = int(request.POST['available_slots']),
                                            is_active=True,
                                            is_delete=False)
                response = {
                        'status':200,
                        'message': "success",
                        'data':{'message':"Drive added Successfully",'drive':{'pk':one.pk,'name':one.vaccine_name,'Class_id':one.Class_id.pk,'class_name':one.Class_id.name,'drive_date':one.drive_date,'available_slots':one.available_slots,'created_at':one.created_at}}
                    }
                return Response(response,status=status.HTTP_200_OK)
            else:
                response = {
                        'status':400,
                        'message': "failed",
                        'data':{'message':"Enter valid Drive Date !"}
                    }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

        else:
            response = {
                    'status':400,
                    'message': "failed",
                    'data':{'message':"Drive Already Exists !"}
                }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST',])
# @authentication_classes([TokenAuthentication])
# @permission_classes((IsAuthenticated,))
# def update_drive(request,pk):
#     drive_obj = Vaccine_Drives.objects.get(pk=pk)
#     if request.method == "POST":
#         drive_obj.drive_date = request.POST['drive_date']
#         drive_obj.available_slots = int(request.POST['available_slots'])
#         drive_obj.is_active = request.POST['is_active']
#         drive_obj.save()
#         response = {
#             'status':200,
#             'message': "success",
#             'data':{'message':"Drive Updated Successfully",'drive':{'pk':drive_obj.pk,'name':drive_obj.vaccine_name,'Class_id':drive_obj.Class_id.pk,'class_name':drive_obj.Class_id.name,'drive_date':drive_obj.drive_date,'available_slots':drive_obj.available_slots,'created_at':drive_obj.created_at}}
#         }
#         return Response(response,status=status.HTTP_200_OK)


@api_view(['POST',])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated,))
def update_drive(request,pk):
    drive_obj = Vaccine_Drives.objects.get(pk=pk)
    if request.method == "POST":
        try:
            drive_date = datetime.strptime(request.POST['drive_date'],'%Y-%m-%d')
            if drive_date > date.today():
                drive_obj.drive_date = drive_date
            else:
                response = {
                    'status':400,
                    'message': "failed",
                    'data':{'message':"Drive date Can't change !"}
                }
                return Response(response,status=status.HTTP_400_BAD_REQUEST)
        except MultiValueDictKeyError:
            pass
        drive_obj.available_slots = int(request.POST['available_slots'])
        drive_obj.is_active = request.POST['is_active']
        drive_obj.save()
        response = {
            'status':200,
            'message': "success",
            'data':{'message':"Drive Updated Successfully",'drive':{'pk':drive_obj.pk,'name':drive_obj.vaccine_name,'Class_id':drive_obj.Class_id.pk,'class_name':drive_obj.Class_id.name,'drive_date':drive_obj.drive_date,'available_slots':drive_obj.available_slots,'created_at':drive_obj.created_at}}
        }
        return Response(response,status=status.HTTP_200_OK)

@api_view(['GET',])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated,))
def delete_drive(request,pk):
    drive_obj = Vaccine_Drives.objects.get(pk=pk)
    drive_obj.is_delete = True
    drive_obj.save()
    response = {
            'status':200,
            'message': "success",
            'data':{'message':"Drive Deleted Successfully"}
        }
    return Response(response,status=status.HTTP_200_OK)

@api_view(['GET',])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated,))
def student_vaccine_data(request):
    all_data = Students_Vaccination.objects.all().order_by('-created_at')
    vaccine_data = []
    for one in all_data:
        vaccine_data.append({'pk':one.pk,'student_name':one.Student_id.name,'student_id':one.Student_id.student_id,'class_name':one.Student_id.Class_id.name,
        'vaccine_name':one.Vaccine_id.vaccine_name,'is_vaccinated':True,'vaccine_date':one.vaccination_date})

    response = {
                'status':200,
                'message': "success",
                'data':{'vaccine_data':vaccine_data}
            }
    return Response(response,status=status.HTTP_200_OK)


@api_view(['POST',])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated,))
def add_student_vaccine(request):
    if request.method == "POST":
        student_obj = Student.objects.get(pk=int(request.POST['student_id']))
        vaccine_obj = Vaccine_Drives.objects.get(pk=int(request.POST['vaccine_id']))
        vaccination_date = request.POST['vaccination_date']
        if not Students_Vaccination.objects.filter(Student_id=student_obj,Vaccine_id=vaccine_obj).exists():
            one = Students_Vaccination.objects.create(Student_id=student_obj,Vaccine_id=vaccine_obj,vaccination_date=vaccination_date)
            vaccine_data = {'pk':one.pk,'student_name':one.Student_id.name,'student_id':one.Student_id.student_id,'class_name':one.Student_id.Class_id.name,
            'vaccine_name':one.Vaccine_id.vaccine_name,'is_vaccinated':one.is_vaccinated,'vaccine_date':one.created_at.date}
            response = {
                'status':200,
                'message': "success",
                'data':{'vaccine_data':vaccine_data}
            }
            return Response(response,status=status.HTTP_200_OK)
        else:
            response = {
                    'status':400,
                    'message': "failed",
                    'data':{'message':"Data Already Exists !"}
                }
            return Response(response,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST',])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated,))
def student_vaccination_upload(request):
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
                if Student.objects.filter(pk=int(row['student_id'])).exists():
                    student_obj = Student.objects.get(pk=int(row['student_id']))
                    if Vaccine_Drives.objects.filter(pk=int(row['vaccine_id'])).exists():
                        vaccine_obj = Vaccine_Drives.objects.get(pk=int(row['vaccine_id']))
                        if not Students_Vaccination.objects.filter(Student_id=student_obj,Vaccine_id=vaccine_obj).exists():
                            Students_Vaccination.objects.create(Student_id=student_obj,Vaccine_id=vaccine_obj,vaccination_date=row['vaccination_date'])
                        else:
                            i = i + 1
                            unupload_data.append({'student_id':row['student_id'],'vaccine_id':row['vaccine_id'],'vaccination_date':row['vaccination_date'],'reason':'Data Already exists !'})
                    else:
                        i = i + 1
                        unupload_data.append({'student_id':row['student_id'],'vaccine_id':row['vaccine_id'],'vaccination_date':row['vaccination_date'],'reason':"Vaccine Drive id doesn't exists !"})

                else:
                    i = i + 1
                    unupload_data.append({'student_id':row['student_id'],'vaccine_id':row['vaccine_id'],'vaccination_date':row['vaccination_date'],'reason':"Student id doesn't exists !"})

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


@api_view(['get',])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated,))
def count_api(request):
    total_student = Student.objects.filter(is_delete=False).count()
    ttl_data_count = Students_Vaccination.objects.all().count()
    drives = Vaccine_Drives.objects.filter(is_active=True,is_delete=False,drive_date__gte=date.today()).count()
    month_count = Students_Vaccination.objects.filter(vaccination_date__month=date.today().month,vaccination_date__year=date.today().year).count()
    total_slots = Vaccine_Drives.objects.filter(is_delete=False).aggregate(Sum('available_slots'))['available_slots__sum']
    percent_no = ((ttl_data_count*100)/total_slots)
    response = {
            'status':200,
            'message': "success",
            'data':{'total_student':total_student,'ttl_data_count':ttl_data_count,'drives':drives,'month_count':month_count,'percent_no':round(percent_no,2)}
        }
    return Response(response,status=status.HTTP_200_OK)



@api_view(['POST',])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated,))
def vaccination_report(request):
    if request.method == "POST":
        start_date = datetime.strptime(request.POST['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(request.POST['end_date'], '%Y-%m-%d')
        vaccine_ids = []
        class_ids = []
        if int(request.POST['vaccine_id']) == 0:
            vaccine_objects = Vaccine_Drives.objects.filter(is_active=True,is_delete=False)
            for one in vaccine_objects :
                vaccine_ids.append(one.pk)
        else:
            vaccine_ids.append(int(request.POST['vaccine_id']))
        if int(request.POST['class_id']) == 0:
            classes_objects = Classes.objects.filter(is_delete=False)
            for one in classes_objects:
                class_ids.append(one.pk)
        else:
            class_ids.append(int(request.POST['class_id']))
        vaccine_data = []
        if Students_Vaccination.objects.filter(Student_id__Class_id__pk__in=class_ids,Vaccine_id__pk__in=vaccine_ids,vaccination_date__range=[start_date,end_date]).exists():
            data_objects = Students_Vaccination.objects.filter(Student_id__Class_id__pk__in=class_ids,Vaccine_id__pk__in=vaccine_ids,vaccination_date__range=[start_date,end_date])
            for one in data_objects:
                vaccine_data.append({'pk':one.pk,'student_name':one.Student_id.name,'student_id':one.Student_id.student_id,'class_name':one.Student_id.Class_id.name,
                'vaccine_name':one.Vaccine_id.vaccine_name,'is_vaccinated':True,'vaccine_date':one.vaccination_date})

        response = {
                'status':200,
                'message': "success",
                'data':{'vaccine_data':vaccine_data}
            }
        return Response(response,status=status.HTTP_200_OK)

@api_view(['GET',])
@authentication_classes([TokenAuthentication])
@permission_classes((IsAuthenticated,))
def export_vaccination_data(request):
    header = ['Vaccine Date','Student Name','Student id','Class Name','Vaccine Name','Status']
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Vaccination_data.xls"'
    row_data = []
    all_data = Students_Vaccination.objects.all().order_by('-created_at')
    for one in all_data:
        row_data.append([one.vaccination_date.strftime("%Y-%m-%d"),one.Student_id.name,one.Student_id.student_id,one.Student_id.Class_id.name,one.Vaccine_id.vaccine_name,"YES"])
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Data")
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True,

    for col_num in range(len(header)):
        ws.write(row_num,col_num,header[col_num],font_style)

    font_style = xlwt.XFStyle()
    for row in row_data:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num,col_num,row[col_num],font_style)
    wb.save(response)
    return response
