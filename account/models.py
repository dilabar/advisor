from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.
class User(AbstractUser):
    full_name=models.CharField(max_length=50,blank=True,null=True)
    user_type = models.IntegerField(default=0, null=True)# 0 =user,1=admin

    def __str__(self):
        return self.username

    def get_tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
class Advisor(models.Model):
    full_name=models.CharField(max_length=50,blank=True,null=True)
    image = models.ImageField (upload_to='advisor_img/',blank=True,null=True)
    created_by = models.IntegerField(default=1, null=True)# 0 =user,1=admin
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    def __str__(self):
        return self.full_name

    def get_image(self):
        return self.image if self.image else " "

class Booking(models.Model):
    advisor_id = models.ForeignKey(Advisor, on_delete=models.CASCADE, related_name='advisor_id')
    booked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_id')
    booked_date = models.DateTimeField(blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    def __str__(self):
        return str(self.id)