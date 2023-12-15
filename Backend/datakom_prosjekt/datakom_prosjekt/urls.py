"""
URL configuration for datakom_prosjekt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from rest_framework import routers
from blodtrykk.views import dashboard, access_view, redirect_if_user_is_super, PostDailyBloodPressureData, LoginView, RegisterView, RegisterPatientView, GetDailyBloodPressureData, PostDailyOxygenSaturationData
from django.contrib import admin
from django.urls import include, path


from blodtrykk.views import PatientViewSet, NurseUserViewSet, patients_list_view, patients_data_view, LogOutView, CookieTokenObtainPairView, CookieTokenRefreshView, CookieTokenVerifyView


router = routers.DefaultRouter()
router.register(r'Patients', PatientViewSet, basename='Patients')
router.register(r'Nurses', NurseUserViewSet, basename='nurse_user')

#The different urls/endpoints for the project
urlpatterns = [
     
    #The root of the api
    path('api/', include(router.urls)), 
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    #The two endpoints for posting ESP32 data
    path('api/post_blood_pressure_data/', PostDailyBloodPressureData,
         name='post-blood-pressure-data'),
    path('api/post_oxygen_saturation_data/',
         PostDailyOxygenSaturationData, name="daily-oxygen-saturation-data"),
    
    #Used for login, logout and registration
    path('api/login/', LoginView.as_view(), name="login"),
    path('api/register/', RegisterView.as_view(), name="register"),
    path('api/logout/', LogOutView.as_view(), name="logout"),
    path('api/register-patient/', RegisterPatientView.as_view(),
         name="register-patient"),

    path('patient/<int:patient_id>/bloodpressure/',
         GetDailyBloodPressureData, name="bloodpressure"),
    
    #The three endpoints for getting, refreshing and verifying the JWT token
    path("api/token/", CookieTokenObtainPairView.as_view(),
         name="token_obtain_pair"),
    path("api/token/refresh/", CookieTokenRefreshView.as_view(), name="token_refresh"),
    path('api/token/verify/', CookieTokenVerifyView.as_view(), name='token_verify'),




    #Not in use
    path('admin/', admin.site.urls),
    path('dashboard/', dashboard, name='dashboard'),
    path("access_view/", access_view, name="access_view"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("redirect_if_user_is_super/", redirect_if_user_is_super,
         name="redirect_if_user_is_super"),
    path("patients/", patients_list_view, name="patients"),
    path('patients/<int:pk>/', patients_data_view, name='patients-data'),
   

]
urlpatterns += router.urls
