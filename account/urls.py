from django.contrib import admin
from django.urls import path
from account.webservice import advisor

urlpatterns = [
    # path('advisor', admin.site.urls),
    path('advisor/', advisor.CreateAdvisorView.as_view(), name='add-advisor'),
    
]
