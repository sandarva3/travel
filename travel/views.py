from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from django.http import JsonResponse
from .utils2 import run_get_summaries
from .utils3 import run_get_places_recommendation
from travel.utils1 import get_nearby_filtered_places
import json
from django.views.decorators.csrf import csrf_exempt


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
    



def get_places_recommendation_view(request):
    try:
        personalized_places = run_get_places_recommendation()
        return JsonResponse({"Best places for you":personalized_places}, safe=False, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)




@csrf_exempt
def get_best_nearby_places_to_visit_view(request):
    try:
            data = request.POST
            longitude = data.get("lng")
            latitude = data.get("lat")
            filtered_places = get_nearby_filtered_places(longitude, latitude)
            run_get_summaries(filtered_places)
            personalized_places = run_get_places_recommendation(filtered_places)
            return JsonResponse({"Best places for you":personalized_places}, safe=False, status=200)
    except Exception as e:
        print(f"In travel/views.get_best_nearby_places_to_visit() ERROR OCCURED: {e}")
        return JsonResponse({"error": str(e)}, status=500)
