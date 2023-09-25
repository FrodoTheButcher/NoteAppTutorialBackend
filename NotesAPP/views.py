from django.shortcuts import render
from rest_framework.decorators import api_view,APIView
from .models import Note
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg.utils import swagger_auto_schema
from django.core.exceptions import ObjectDoesNotExist
from .serializers import NoteSerializer


class NoteView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            
            type=openapi.TYPE_OBJECT,
            properties={
                "name":openapi.Schema(type=openapi.TYPE_STRING),
                "description":openapi.Schema(type=openapi.TYPE_STRING),
                "user":openapi.Schema(type=openapi.TYPE_STRING),
                "expireDate":openapi.Schema(type=openapi.TYPE_STRING)
            }
        )
)
    def post(self,request):
        try:
            data = request.data
            serializer = NoteSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"data":"success"},status=status.HTTP_201_CREATED)
            else:
                errors = serializer.errors
                return Response({"errors":errors},status=status.HTTP_400_BAD_REQUEST)        
        except Exception as e:
            return Response({"data":"Server exception"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            
            type=openapi.TYPE_OBJECT,
            properties={
                "user":openapi.Schema(type=openapi.TYPE_STRING),
                "name":openapi.Schema(type=openapi.TYPE_STRING),
                "description":openapi.Schema(type=openapi.TYPE_STRING),
            }
        )
    )
    def put(self,request,pk):
        try:
            data = request.data
            note = Note.objects.get(id=pk)
            serializedNote = NoteSerializer(instance=note,data=data)
            if serializedNote.is_valid():
                serializedNote.save()
                return Response({"data":"Success"},status=status.HTTP_200_OK)
            else:
                errors = serializedNote.errors
                return Response({"errors":errors},status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            return Response({"data":"Id not found"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"data":"Server exception"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def get(self,request,pk=None):
        if pk is None:
            try:
                notes = Note.objects.all()
                convertedNotes = NoteSerializer(notes,many=True)
                #convert the notes
                return Response({"data":convertedNotes.data},status=status.HTTP_200_OK)
            except ObjectDoesNotExist as e:
                return Response({"data":"Id not found"},status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(e)
                return Response({"data":"Server exception"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            try:
                    note = Note.objects.get(id=pk)
                    convertedNote = NoteSerializer(note,many=False)
                    return Response({"data":convertedNote.data},status=status.HTTP_200_OK)
            except ObjectDoesNotExist as e:
                    return Response({"data":"Id not found"},status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                    print(e)
                    return Response({"data":"Server exception"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                