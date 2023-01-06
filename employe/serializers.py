from .models import Employe,ExcelFileUpload,Appointment
from .models import User
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
import pandas as pd

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'first_name', 'last_name', 'email','password')

class ExcelFile(serializers.ModelSerializer):
    class Meta:
        model = ExcelFileUpload
        fields = '__all__'

    def create(self, validated_data):
        data = validated_data.pop('excel_file')
        df = pd.read_excel(data)
        for index in df.index:
            print(df['firstname'][index])
            exists = User.objects.filter(email=df['email'][index]).exists()
            if not exists:
                user = User.objects.create(
                    username=df['username'][index],
                    first_name = df['firstname'][index],
                    last_name = df['lastname'][index],
                    email = df['email'][index],
                    password = make_password(df['password'][index]),
                )
                user.save()
                employe = Employe.objects.create(
                    user = user,
                    phoneno = df['phoneno'][index],
                    age = df['age'][index],
                    status = df['status'][index],
                    industry = df['industry'][index],
                    description = df['description'][index],
                    image = df['image'][index],
                )
                employe.save()
        return df

class EmployeSerializer(serializers.ModelSerializer):
    user = UserSerializer(required = True)
    # appointment = AppointmentSerializer(many=True)
    # appointment = 
    class Meta:
        model = Employe
        fields = '__all__'

    def create(self, validated_data):
        print("Validated Data is:",validated_data)
        # user_data = validated_data.pop('user')
        
        # employe = Employe.objects.create(**validated_data)
        # print("Employe Created is :",employe)
        # User.objects.create(user=employe, **user_data)
        # return employe     
        user_data = validated_data.pop('user')
        password = make_password(user_data.pop('password'))
        print("user data is:",user_data)
        # print("password is",user)
        # print("Data Type is :",type(user))
        user = User.objects.create(password=password, **user_data)
        print("store user data",user)
        employe = Employe.objects.create(user=user,**validated_data)
        # print("steric Data is:",**validated_data)
        # user = Employe.objects.create(**validated_data)
        # print("User is:",user)
        # User.objects.create(, **user_data)
        # employe, created = Employe.objects.update_or_create(user=user,
                            # subject_major=validated_data.pop('user'))
        return employe

    def update(self, instance, validated_data):
        tasks = validated_data.pop("user")
        us  = instance.user
        instance = super().update(instance, validated_data)
        us.username = tasks.get('username', us.username)
        us.first_name = tasks.get('first_name', us.first_name)
        us.last_name = tasks.get('last_name', us.last_name)
        us.email = tasks.get('email', us.email)
        us.password = tasks.get('password', us.password)
        us.save()
        return instance

class AppointmentSerializer(serializers.ModelSerializer):
    employe = EmployeSerializer(required=True)
    class Meta:
        model = Appointment
        fields = '__all__'

    def create(self, validated_data):
        print("Validated Data is: ",validated_data)
        employe_data = validated_data.pop('employe')
        user_data = employe_data.pop('user')
        user = User.objects.create( **user_data)
        employe = Employe.objects.create(user=user,**employe_data)
        appointment = Appointment.objects.create(employe=employe,**validated_data)
        return appointment
    
    def update(self, instance, validated_data):
        employe_data = validated_data.pop('employe')
        user = employe_data.pop("user")
        employe  = instance.employe
        us = employe.user
        instance = super().update(instance, validated_data)
        us.username = user.get('username', us.username)
        us.first_name = user.get('first_name', us.first_name)
        us.last_name = user.get('last_name', us.last_name)
        us.email = user.get('email', us.email)
        us.password = user.get('password', us.password)
        us.save()
        return instance
