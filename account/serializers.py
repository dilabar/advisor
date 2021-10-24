from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from account.models import *
from base64 import urlsafe_b64decode
import base64
from django.conf import settings

def encode_image_base64(full_path):
    image = ''
    if full_path != "":
        with open(full_path, 'rb') as imgFile:
            image = base64.b64encode(imgFile.read())
    return image 

    
class AdvisorCreateSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(max_length=50, required=True)
    image = serializers.ImageField(allow_empty_file=False)

    class Meta:
        model = Advisor
        fields = ('full_name', 'image')
class AdvisorViewSerializer(serializers.ModelSerializer):


    class Meta:
        model = Advisor
        fields = ('id','full_name', 'image')

class UserCreateSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(max_length=50, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )


    class Meta:
        model = User
        fields = ('full_name', 'email','password')
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )


    class Meta:
        model = User
        fields = ('email','password')
class BookingCreateSerializer(serializers.ModelSerializer):
    booked_date=serializers.DateTimeField(required=True)
    # booked_by=serializers.CharField(required=False,write_only=False)
    # advisor_id=serializers.CharField(required=False,write_only=False)
    class Meta:
        model=Booking
        fields=['booked_date']

class BookingViewSerializer(serializers.ModelSerializer):
    advisor_image = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields ='__all__'

  
    def to_representation(self,instance):
        
        data={
            'advisor_name':instance.advisor_id.full_name,
            'advisor_image':instance.advisor_id.image.url,
            'advisor_id':instance.advisor_id.id,
            'booking_time':instance.booked_date,
            'booking_id':instance.id,
        }
      
        return data


