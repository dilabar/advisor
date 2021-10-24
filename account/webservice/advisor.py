
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from account.serializers import AdvisorCreateSerializer, AdvisorViewSerializer, BookingCreateSerializer, BookingViewSerializer, UserCreateSerializer, UserLoginSerializer
from account.models import Advisor, Booking, User
import random
from django.contrib.auth import get_user_model
class CreateAdvisorView (APIView,):
    ''' create advisor'''
    serializer_class = AdvisorCreateSerializer

    def post(self,request,format=None):
        ser = self.serializer_class (
            data=request.data,
            context={'request': request}
        )
        if ser.is_valid ():
            ser.save()
            return Response ({'result': True,'msg': "success"},status=status.HTTP_200_OK)

        return Response ( {'result': False,'error':  ser.errors},status=status.HTTP_400_BAD_REQUEST)


class CreateUserView (APIView,):
    ''' create user'''
    serializer_class = UserCreateSerializer

    def post(self,request,format=None):
        ser = self.serializer_class (
            data=request.data,
            context={'request': request}
        )
        if ser.is_valid ():
      
            email = request.data.get ("email")
            full_name = request.data.get ("full_name")
            password = request.data.get ("password")
            username = email.split("@")[0]
            user = User.objects.filter(email=email,user_type=0).count()            
            usernm = User.objects.filter(username=username,user_type=0).count()
            if usernm>0:
                username=username+str(random.randint(1000, 9999))
            if user > 0:
                msg = {"Unauthorized error ": ['Email already Registered....', ]}
                errors = {'errors': msg}
                return Response(errors, status=401)
            else:
                obj = User.objects.create_user( 
                    email=email,
                    username=username,
                    is_staff=False,
                    is_superuser=False,
                    is_active=True,
                    user_type=0
                )
                obj.set_password(password)
                obj.save()
                data = {
                    'user_id': obj.id,
                    'token':obj.get_tokens()
                   
                }


       
           
            return Response ({'result': True,'msg': "User created successfully",'body':data},status=status.HTTP_200_OK)

        return Response ( {'result': False,'error':  ser.errors},status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView,):
    serializer_class = UserLoginSerializer

    def post(self, request,format=None):
        ser = self.serializer_class (
            data=request.data,context={'request': request}
        )
      
        if ser.is_valid():
            email = request.data['email']
            password = request.data['password']
            User = get_user_model()
            user = User.objects.filter(email=email,user_type=0).first()
            if user:
                if user.check_password(password):
                    data={
                        'user_id': user.id,
                        'token':user.get_tokens()
                    }
                    return Response ({'result': True,'msg': "Login successfully",'body':data},status=status.HTTP_200_OK)

            else:
                return Response({'result': False, 'msg': 'Email or Password did not match'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response ( {'result': False,'error':  ser.errors},status=status.HTTP_400_BAD_REQUEST)


class AdvisorListView(generics.ListAPIView):
    queryset = Advisor.objects.all()
    # serializer_class = AdvisorViewSerializer
    # permission_classes = [IsAdminUser]

    def list(self, request,user_id):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = AdvisorViewSerializer(queryset, many=True)
        return Response ({'result': True,'body':serializer.data},status=status.HTTP_200_OK)



class CreateBookingView (APIView,):
    ''' booking  advisor call'''
    serializer_class = BookingCreateSerializer

    def post(self,request,user_id,advisor_id,format=None):

        ser = self.serializer_class (
            data=request.data,
            context={'request': request}
        )
        user = User.objects.filter(id=user_id,user_type=0).count() 
     
        if user <= 0:
            msg = {"Bad request ": ['user not found', ]}
            errors = {'errors': msg}
            return Response(errors, status=404)
        adv = Advisor.objects.filter(id=advisor_id).count() 
        if adv <= 0:
            msg = {"Bad request ": ['advisor not found', ]}
            errors = {'errors': msg}
            return Response(errors, status=404)

        if ser.is_valid ():
            # print(ser,user_id)
            booked_date=request.data['booked_date']
           
            B=Booking.objects.create(booked_date=booked_date,booked_by_id=user_id,advisor_id_id=advisor_id)
            return Response ({'result': True,'msg': "success"},status=status.HTTP_200_OK)

        return Response ( {'result': False,'error':  ser.errors},status=status.HTTP_400_BAD_REQUEST)

class BookingListView(generics.ListAPIView):
    queryset = Booking.objects.all()
    # serializer_class = BookingViewSerializer
    # permission_classes = [IsAdminUser]

    def list(self, request,user_id):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = BookingViewSerializer(queryset, many=True)
        return Response ({'result': True,'body':serializer.data},status=status.HTTP_200_OK)
