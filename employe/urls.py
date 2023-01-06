from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register('employeApi',views.EmployeViewSet,basename="employeView")
router.register('excelFileApi',views.ExcelFileViewSet,basename="excelfileView")
router.register('appointment',views.AppointmentViewSet)
urlpatterns = [
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='password_reset.html'),name="reset_password"),
    path('register/',views.registerUser,name='registeruser'),
    path('<int:id>',views.registerUser,name='register'),
    path('login/',views.login,name='login'),
    path('edit/',views.edit,name='edit'),
    path('index/',views.index,name='index'),
    path('exportexcel/',views.exportexcel,name='exportexcel'),
    path('importexcel/',views.importexcel,name='importexcel'),
    path('',include(router.urls),name='route')
    # path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'),name="password_reset_done"),
    # path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_form.html'),name="password_reset_confirm"),
    # path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'),name="password_reset_complete"), 
]