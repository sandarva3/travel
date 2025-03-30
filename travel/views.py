from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from django.http import JsonResponse
from .utils import run_get_summaries
from .utils2 import get_all_places
from .utils3 import start
import json

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



def get_summaries_view(request):
    try:
        run_get_summaries()
        return JsonResponse({"msg": "Summaries processed successfully."}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    


def get_all_places_view(request):
    try:
        all_places = get_all_places()
        length = len(all_places)
        print(f"length: {length}")
        return JsonResponse(all_places, safe=False, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



def get_personalized_places_view(request):
    try:
        personalized_places = start()
        print(personalized_places)
        return JsonResponse(personalized_places, safe=False, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
