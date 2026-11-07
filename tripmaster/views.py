from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from tripmaster.serializers import userserializer,tripSerializers
from django.contrib.auth.models import User
from tripmaster.models import Tripdb
from rest_framework import authentication,permissions,serializers
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
# Create your views here.
class signupview(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        form_data=request.data
        insta_serilizers=userserializer(data=form_data)
        if insta_serilizers.is_valid():
            insta_serilizers.save()
            return Response(data={"message":"user created sucess"},status=200)
        else:
            return Response(data=insta_serilizers.errors,status=400)

class TripCreateUpdateView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    authentication_classes=[authentication.BasicAuthentication]
    def get(self,request):
         qs=Tripdb.objects.filter(created_by=request.user.id)
         seri_insta=tripSerializers(qs,many=True)
         return Response(data=seri_insta.data,status=200)
    def post(self,request):
        form_data=request.data
        insta_serialzers=tripSerializers(data=form_data)
        if insta_serialzers.is_valid():
            insta_serialzers.save(created_by=request.user)
            return Response(data={"message":"trip created sucess",
                                  "trip":insta_serialzers.data},status=200)
        else:
                return Response(data=insta_serialzers.errors,status=400)

class TripRetriveUpdateDeleteView(APIView):
            permission_classes=[permissions.IsAuthenticated]
            authentication_classes=[authentication.BasicAuthentication]
            def get(self,request,pk):
                trip=get_object_or_404(Tripdb,pk=pk)
                if trip.created_by==request.user:
                    serilaizer_ins=tripSerializers(trip)
                    return Response(serilaizer_ins.data)
                else: raise serializers.ValidationError("Your are not allowed to acess this data")
            def put(self,request,pk,):
                 trip_obj=get_object_or_404(Tripdb,id=pk)
                 if trip_obj.created_by!=request.user:
                      raise serializers.ValidationError("Not allowed to Edit This Data")
                 else:
                      form_data=request.data
                      seri_insta=tripSerializers(data=form_data,instance=trip_obj)
                      if seri_insta.is_valid():
                           seri_insta.save()
                           return Response(data={"message":"data edited scuess",
                                            "tripDetails":seri_insta.data})
                      else:Response(data=seri_insta.errors)
            def delete(self,request,pk):
                 trip_obj=get_object_or_404(Tripdb,id=pk)
                 if trip_obj.created_by !=request.user:
                      raise serializers.ValidationError("No acesss ti delete this data" )
                 else:
                      trip_obj.delete()
                      return Response(data={"message":"deleted trip scuess"})
                    
                 
                     
                      

                 
                
         

            