from django.shortcuts import render
from rest_framework.decorators import api_view, APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.core.exceptions import ObjectDoesNotExist
from .serializers import UserSerializer , UserSerializerUpdate


class UserView(APIView):
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            
            type=openapi.TYPE_OBJECT,
            properties={
                "username":openapi.Schema(type=openapi.TYPE_STRING),
                "email":openapi.Schema(type=openapi.TYPE_STRING),
                "password":openapi.Schema(type=openapi.TYPE_STRING),
                "password2":openapi.Schema(type=openapi.TYPE_STRING)
            }
        )
)
    def post(self,request):
         try:
            data = request.data
            password2 = data['password2']
            password1 = data['password']
            if password1 != password2:
                return Response({"errors":"passwords must match"},status=status.HTTP_400_BAD_REQUEST)
            
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"data":"Success"},status=status.HTTP_200_OK)
            else:  
                errors = serializer.errors
                return Response({"errors":errors},status=status.HTTP_400_BAD_REQUEST)
         except Exception as e:
            return Response({"errors":"Server exception"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    @swagger_auto_schema(
        request_body=openapi.Schema(
            
            type=openapi.TYPE_OBJECT,
            properties={
                "email":openapi.Schema(type=openapi.TYPE_STRING),
                "username":openapi.Schema(type=openapi.TYPE_STRING),
            }
        )
)
    def put(self,request,pk):
        try:
            data = request.data
            user = User.objects.get(id=pk)
            serializer = UserSerializerUpdate(instance=user,data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"data":"Success"},status=status.HTTP_200_OK)
            else:
                errors = serializer.errors
                return Response({"errors":errors},status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            return Response({"data":"Id not found"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"data":"Server exception"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def get(self,request,pk=None):
        if pk is None:
            try:
                users = User.objects.all()
                usersSerialized = UserSerializer(users,many=True)
                return Response({"data":usersSerialized.data},status=status.HTTP_200_OK)
            except ObjectDoesNotExist as e:
                return Response({"data":"Id not found"},status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(e)
                return Response({"data":"Server exception"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            try:
                user = User.objects.get(id=pk)
                userSerialized = UserSerializer(user,many=False)
                return Response({"data":userSerialized.data},status=status.HTTP_200_OK)
            except ObjectDoesNotExist as e:
                return Response({"data":"Id not found"},status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(e)
                return Response({"data":"Server exception"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

         

    def delete(self,request,pk):
        try:
              user = User.objects.get(id=pk)
              user.delete()
              return Response({"data":"Success"},status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return Response({"data":"Id not found"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"data":"Server exception"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


