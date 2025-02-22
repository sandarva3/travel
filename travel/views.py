from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer



class UserRegistration_view(APIView):
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid(): #This method checks the validity of input data on our defined model on UserSerializer(like data type, length, everything). 
        # and if valid, returns a dictionary object, and through that dictionary objects values we create user instance.
            user = serializer.save() #calls create() in UserSerializer
            print(f"User created: {user}. ID: {user.id}")
            return Response({'msg': 'User created successfully.'})
        print("User not created")
        return Response({'msg': serializer.errors})