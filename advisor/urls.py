"""advisor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from account.webservice import advisor
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('dadmin/', admin.site.urls),
    path('admin/',include('account.urls')),
    path('user/register/', advisor.CreateUserView.as_view(), name='add-user'),
    path('user/login/', advisor.UserLoginView.as_view(), name='user-login'),
    path('user/<user_id>/advisor/', advisor.AdvisorListView.as_view(), name='user-advisor'),
    path('user/<int:user_id>/advisor/<int:advisor_id>/', advisor.CreateBookingView.as_view(), name='booking-advisor'),
    path('user/<int:user_id>/advisor/booking/', advisor.BookingListView.as_view(), name='booking-list'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
