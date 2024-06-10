from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, VerifyOTPSerializer , FeedbackSerializer
from .models import User
import random
from .utils import send_email_to_client, send_feedback_to_client, send_password_change_to_client


class UserRegistrationView(APIView):
    # Register User
    def post(self,request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                otp = random.randint(100000, 999999)
                send_email_to_client(otp,request.data['email'])
                new_user_data = User.objects.filter(email=request.data['email'])
                user_data = {
                "id": new_user_data.first().id,
                "first_name": new_user_data.first().first_name,
                "last_name": new_user_data.first().last_name,
                "email": new_user_data.first().email,
                "phone_number": new_user_data.first().phone_number,
                "verified": new_user_data.first().verified,
                "is_active": new_user_data.first().is_active,
                "user_points": new_user_data.first().user_points
            }
                return Response({"status":201,"message": "User registered successfully.Please Verify Your email using otp sent to your mail", "user_data" : user_data}, status=status.HTTP_201_CREATED)
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message": serializer.error_messages},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": e}, status=status.HTTP_400_BAD_REQUEST)

    # Update User
    def put(self, request, pk):
        try:
            userdata = User.objects.get(id=pk)
            serializer = UserSerializer(instance=userdata,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User updated successfully."}, status=status.HTTP_200_OK)
            return Response({"message": "Some Errors"},serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": e}, status=status.HTTP_400_BAD_REQUEST)

    # Delete User
    def delete(self, request, pk):
        userdata = User.objects.get(id=pk)
        userdata.delete()
        return Response({"message": "User deleted successfully."}, status=status.HTTP_200_OK)

    # Get All Users
    def get(self,request):
        userdata = User.objects.all().using('default')
        serializer = UserSerializer(userdata, many=True)
        return Response({"all_users":serializer.data})

class LoginUser(APIView):
    def post(self, request):
        try:
            data = request.data
            user = User.objects.filter(email=data['email'])
            user_data = {
                "id": user.first().id,
                "first_name": user.first().first_name,
                "last_name": user.first().last_name,
                "email": user.first().email,
                "phone_number": user.first().phone_number,
                "verified": user.first().verified,
                "is_active": user.first().is_active,
                "user_points": user.first().user_points
            }
            if not user.exists():
                return Response({"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
            user = user.first()
            if user.password != data['password']:
                return Response({"message": "Invalid Password"}, status=status.HTTP_400_BAD_REQUEST)
            if not user.verified:
                return Response({"message": "User not verified", "user_data":user_data}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "User logged in successfully", "user_data":user_data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Some Error Occured"}, status=status.HTTP_400_BAD_REQUEST)

class ForgetPass(APIView):
    def post(self, request):
        try:
            data = request.data
            user = User.objects.filter(email=data['email'])
            if data["email"] != user.first().email:
                return Response({"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                password = data['password']
                user = user.first()
                user.password = password
                user.save()
                send_password_change_to_client(password,data['email'])
                return Response({"status":200, "message": "Password Changed"})
        except Exception as e:
            return Response({"message": "Some Error Occured"}, status=status.HTTP_400_BAD_REQUEST)

# Verify User
class VerifyOTP(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = VerifyOTPSerializer(data=data)

            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']
                user = User.objects.filter(email=email)
                if not user.exists():
                    return Response({"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
                if user[0].otp != otp:
                    return Response({"message": "Not a valid OTP"}, status=status.HTTP_400_BAD_REQUEST)
                user = user.first()
                user.verified = True
                user.save()
                return Response({"message": "User verified successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Some Error Occured"}, status=status.HTTP_400_BAD_REQUEST)

# Retry OTP
class RetryOTP(APIView):
    def post(self, request):
        otp = random.randint(100000, 999999)
        send_email_to_client(otp,request.data['email'])
        return Response({"status":200,"message": "OTP Sent. Please Verify Your email using otp sent to your mail"})


class UserPoints(APIView):
    def post(self, request, pk):
        user = User.objects.get(id=pk)
        user.user_points = user.user_points + request.data["user_points"]
        user.save()
        return Response({"message":"Updated User Points are","user_points": user.user_points})


class FeedbackApi(APIView):
    def post(self, request):
        try:
            serializer = FeedbackSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                send_feedback_to_client(request.data['name'],request.data['title'],request.data['about'],request.data['description'],request.data['email'])
                return Response({"status":201,"message": "Feedback Created successfully. We will contact ASAP. Thanks"}, status=status.HTTP_201_CREATED)
            return Response({"status":status.HTTP_400_BAD_REQUEST,"message": serializer.error_messages},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": e}, status=status.HTTP_400_BAD_REQUEST)


class Terminate(APIView):
    def post(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            if user.is_active == True:
                user.is_active = False
                user.save()
                return Response({"status":200, "message": "User Terminated successfully", "user_active": user.is_active})
            user.is_active = True
            user.save()
            return Response({"status":200, "message": "User Activated", "user_active": user.is_active})
        except Exception as e:
            return Response({"message": "Some Error Occured", "Error": e}, status=status.HTTP_400_BAD_REQUEST)





