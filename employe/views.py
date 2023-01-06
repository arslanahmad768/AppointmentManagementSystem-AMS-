# Create your views here.
from rest_framework.filters import OrderingFilter,SearchFilter
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.decorators import action 
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import EmployeSerializer,ExcelFile,AppointmentSerializer
from .models import Employe,ExcelFileUpload,Appointment,User
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from io import BytesIO

from django.contrib.auth import authenticate 
# Create your views here.

def login(request):
    return render(request,'login.html')

def registerUser(request,id=None):
    return render(request,'registerUser.html',context={"check":id})

def edit(request):
    return render(request,'updateUser.html')

def index(request):
    return render(request,'index.html')

class EmployeViewSet(viewsets.ModelViewSet):
    queryset = Employe.objects.all()
    serializer_class = EmployeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    filter_backends = [ SearchFilter]
    search_fields = ['^user__first_name','user__email','phoneno']

    def log(self,request):
        print("called log function")
        pass

    @action(detail=True, methods=['POST'])
    def loginAuth(self, request,pk=None):
        print("request data is ",request.data)
        email = request.data['email']
        password = request.data['password']
        user_obj = User.objects.filter(email = email)
        if not user_obj.exists():
            content = {'statusText': 'Account not found'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        user_obj = authenticate(email =email,password = password)
        if user_obj and user_obj.is_superuser:
            return Response({"statusText":"successfully execute"},status=status.HTTP_200_OK)
        return Response({"statusText":"Invalid Information"},status=status.HTTP_401_UNAUTHORIZED)
        # user = self.get_object()
        # print(request)
        # print(request.data)
        # serializer = UserSerializer(data=request.data)
        # if serializer.is_valid():
        #     user.set_password(serializer.validated_data['password'])
        #     user.save()
        #     return Response({'status': 'password set'})
        # else:
        #     return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
       
class ExcelFileViewSet(viewsets.ModelViewSet):
    queryset = ExcelFileUpload.objects.all()
    serializer_class = ExcelFile
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['GET'])
    def exportToExcel(self,request):
        if (Employe.objects.all().exists()):
            output = BytesIO()
            data = []
            queryset = Employe.objects.all()
            for obj in queryset:
                data.append({
                    'first_name':obj.user.first_name,
                    'last_name': obj.user.last_name,
                    'email': obj.user.email,
                    'password': obj.user.password,
                    'phoneno': obj.phoneno,
                    'age': obj.age,
                    'status': obj.status,
                    'industry': obj.industry,
                    'description': obj.description,
                    'image': obj.image,
                })

            edf = pd.DataFrame(data) 
            edf.to_excel(output)
            response  = HttpResponse(content_type='application/vnd.ms-excel')
        
            response['Content-Disposition'] = 'attachment; filename="report.xlsx"'
            response.write(output.getvalue())
            return response
        return Response({"statusText":"User Not exist"},status=status.HTTP_404_NOT_FOUND)



def  exportexcel(request):
    pass
def importexcel(request):
    pass

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    filter_backends = [ SearchFilter]
    search_fields = ['^employe__user__first_name','employe__user__email','=employe__phoneno']