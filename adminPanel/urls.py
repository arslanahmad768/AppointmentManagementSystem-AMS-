from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from django.urls import path,include
from . import views


urlpatterns = [
    path('loginpage/',views.loginPage,name='loginPage'),
    path('login/',views.login,name='login'),
    path('jwtToken/',views.MyTokenObtainPairView.as_view()),
    path('refreshToken/',TokenRefreshView.as_view()),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('employePage/',views.EmployeHomePage,name='EmployeHomePage'),
    path('update/',views.UpdateRecord,name='updateRecord'),
    path('add/',views.addRecord,name='addUser'),
    path('<int:id>/',views.addRecord,name='addUser'),
    path('importexcel/',views.importExcel,name='importexcelFile'),
    path("appointmentpage/",views.AppointmentPage,name="appointmentpage")

]