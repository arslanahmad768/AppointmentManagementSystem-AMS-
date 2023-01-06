from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import HttpResponse
from employe.models import User,ExcelFileUpload,Employe
from employe.serializers import ExcelFile

import pandas as pd


# Create your views here.
def loginPage(request):
    return render(request,"loginPage.html")

def dashboard(request):
    return render(request,"dashboard.html")

def EmployeHomePage(request):
    return render(request,'employeHomePage.html')

def addRecord(request,id=None):
    return render(request,'registrationPage.html',context={"check":id})

def importExcel(request):
    return render(request,'excelFile.html')

def UpdateRecord(requst):
    return render(requst,'updatePage.html')

def AppointmentPage(request):
    return render(request,'appointmentPage.html')

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET', 'POST'])
def login(request):
    if request.method == 'POST':
        print("Login Function called")
        email = request.data['email']
        password = request.data['password']
        user_obj = User.objects.filter(email = email)
        if not user_obj.exists():
            content = {'statusText': 'Account Not Found'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        user_obj = authenticate(email =email,password = password)
        if user_obj and user_obj.is_superuser:
            return Response({"statusText":"Successfully Execute"},status=status.HTTP_200_OK)
        return Response({"statusText":"Invalid Information"},status=status.HTTP_401_UNAUTHORIZED)
    return Response({"statusText":"Invalid Data"},status=status.HTTP_401_UNAUTHORIZED)

# @api_view(['GET','POST'])
# def importExceldata(request):
#     if request.method == 'POST':
#         print("request is:",request)
#         file = request.stream.FILES['file']
#         dfs = pd.read_excel(file, sheet_name=None)
#         df = pd.DataFrame(dfs["Sheet1"])
#         print("DataType is",type(df))
#         print("Dict is :",df)
#         for index in df.index:
#             print(df['firstname'][index])
#             exists = User.objects.filter(email=df['email'][index]).exists()
#             if not exists:
#                 user = User.objects.create(
#                     username=df['username'][index],
#                     first_name = df['firstname'][index],
#                     last_name = df['lastname'][index],
#                     email = df['email'][index],
#                     password = df['password'][index],
#                 )
#                 user.save()
#                 employe = Employe.objects.create(
#                     user = user,
#                     phoneno = df['phoneno'][index],
#                     age = df['age'][index],
#                     status = df['status'][index],
#                     industry = df['industry'][index],
#                     description = df['description'][index],
#                     image = df['image'][index],
#                 )
#                 employe.save()
#         return Response({"Result is:":employe})
    