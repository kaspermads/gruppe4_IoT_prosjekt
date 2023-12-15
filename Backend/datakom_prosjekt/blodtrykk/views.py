# Importing the basics
from django.conf import settings
from .models import Patient, DailyBloodPressureData, DailyOxygenSaturationData
from django.urls import reverse
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from django.middleware.csrf import get_token
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


# Importing serializers
from .serializers import PatientListSerializer, PatientDataSerializer, PatientBloodPressureDataSerializer, NurseUserSerializer, UserCreationSerializer, PatientRegisterSerializer, PatientOxygenSaturationDataSerializer

# Importing decorators
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


# Importing authentication and permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny


# Importing forms, such as the built in UserCreationForm
from .forms import CustomUserCreationForm, AccessToRegistrationForm, PatientForm

#The PatientViewSet is used to display the patients in the database while requiring authentication and login
class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientListSerializer
    queryset = Patient.objects.all()
    permission_classes = [IsAuthenticated]

    #Overrides the serializer_class to PatientDataSerializer based on the action
    def get_serializer_class(self):
        if self.action == 'list':
            return PatientListSerializer

        if self.action == 'retrieve':
            return PatientDataSerializer

        return super().get_serializer_class()

    #Overrides the create function to add the user that created the patient
    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)


#Test view for the patient list, not in use.
@permission_classes([IsAuthenticated])
@login_required
def patients_list_view(request):
    patients = Patient.objects.all()
    patients_data = [
        {

            "id": patients.id,
            "first_name": patients.first_name,
            "last_name": patients.last_name,
            "birthDate": patients.birthDate,
            "phone": patients.phone,
            "added_by": patients.added_by,

        } for patients in patients
    ]

    context = {'patients': patients_data}
    return render(request, 'view_patients.html', context)


#Test view for the patient data, not in use.
@permission_classes([IsAuthenticated])
@login_required
def patients_data_view(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    patient_blood_pressure_data = DailyBloodPressureData.objects.all().filter(patient=patient)
    context = {'patient': patient,
               'patient_blood_pressure_data': patient_blood_pressure_data}
    return render(request, 'patient_data.html', context)


#The PostDailyBloodPressureData is used to view the daily bloodpressuredata sent from the ESP32 to the database
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def PostDailyBloodPressureData(request):
    if request.method == 'POST':
        serializer = PatientBloodPressureDataSerializer(data=request.data)
        
        #Checks if the data is valid, and saves it to the database. Maintains data integrity.
        if serializer.is_valid(): 
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


#Handles the post request for the daily oxygen saturation data.
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def PostDailyOxygenSaturationData(request):
    if request.method == 'POST':
        serializer = PatientOxygenSaturationDataSerializer(data=request.data)
        
        #Checks if the data is valid, and saves it to the database. Maintains data integrity.
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def GetDailyBloodPressureData(request, patient_id):
    blood_pressure_data = DailyBloodPressureData.objects.all().filter(patient=patient_id)
    oxygen_saturation_data = DailyOxygenSaturationData.objects.all().filter(patient=patient_id)

    if not blood_pressure_data:
        return Response(status=status.HTTP_404_NOT_FOUND)

    blood_pressure_serializer = PatientBloodPressureDataSerializer(
        blood_pressure_data, many=True)
    oxygen_saturation_serializer = PatientOxygenSaturationDataSerializer(
        oxygen_saturation_data, many=True)

    return Response({
        'blood_pressure_data': blood_pressure_serializer.data,
        'oxygen_saturation_data': oxygen_saturation_serializer.data
    })


class NurseUserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NurseUserSerializer
    queryset = User.objects.all()
    permission_classes = [DjangoModelPermissions]


def dashboard(request):
    return render(request, "dashboard.html")


# The access_view is used to grant access to the registration page
ACCESS_CODE = "2441"


def access_view(request):
    if request.method == 'POST':
        form = AccessToRegistrationForm(request.POST)
        if form.is_valid():
            access_code = form.cleaned_data["access_code"]
            if access_code == ACCESS_CODE:
                request.session["access_granted_to_register"] = True
                return redirect(reverse("register"))
            else:
                form.add_error("access_code", "Wrong access code")
    else:
        form = AccessToRegistrationForm()
    return render(request, "access_form.html", {"form": form})

# The register view is used to register a new nurse


# The register view is used to register a new nurse
def register(request):
    if not request.session.get("access_granted_to_register"):

        return redirect(reverse("access_view"))

    if request.method == "GET":
        return render(
            request, "register_nurse.html",
            {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            login(request, user)
            # fjerner nøkkelen etter vellykket registrering
            del request.session['access_granted_to_register']

            return redirect(reverse("dashboard"))


def redirect_if_user_is_super(request):
    if request.user.is_superuser:
        return redirect('/')
    else:

        return redirect(reverse('dashboard'))

# The register_pasient view is used to register a new pasient


@api_view(['POST'])
def register_patient_test(request):
    if request.method == "GET":
        return render(
            request, "register_patient.html",
            {"form": PatientForm}
        )
    elif request.method == "POST":
        form = PatientForm(request.POST, request.FILES)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.added_by = request.user
            patient.save()

            return redirect(reverse("patients"))
    else:
        form = PatientForm()
    return render(request, "register_patient.html", {"form": form})


class RegisterPatientView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = PatientRegisterSerializer(
            data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(added_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#
class LoginView(APIView):

    #Allows anyone to have access to the endpoint. To demonstrate functionality.
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            response = Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),

            })
            
            response.set_cookie(
                'access',
                str(refresh.access_token),
                httponly=True,
                secure=True,
                samesite='Lax'
                
            )
            return response

        return Response({'error': 'Wrong username or password'}, status=status.HTTP_401_UNAUTHORIZED)


# The LogOutView is used to log out the user by deleting the access and refresh token cookies.
class LogOutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        response = JsonResponse({'detail': 'You are logged out'})
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        return response


#Handles the registration of a new nurse.
class RegisterView(APIView):

    #Allows anyone to have access to the endpoint. To demonstrate functionality.
    permission_classes = [AllowAny]
    serializer_class = UserCreationSerializer

    #If the data is valid, the user is created and a refresh and access token is returned.
    def post(self, request):
        serializer = UserCreationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': {
                    'username': user.username,

                },
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# The CookieJWTAuthentication is used to authenticate the user with the JWT token.
# The three views below are used to get, refresh and verify the token.

class CookieTokenObtainPairView(TokenObtainPairView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('access'):
            response.set_cookie(
                'access',
                response.data['access'],
                httponly=True,
                secure=True,
                samesite='Lax'
            )
            del response.data['access']
        return super().finalize_response(request, response, *args, **kwargs)



class CookieTokenRefreshView(TokenRefreshView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('access'):
            response.set_cookie(
                'access',
                response.data['access'],
                httponly=True,
                secure=True,
                samesite='Lax'
            )
            del response.data['access']
        return super().finalize_response(request, response, *args, **kwargs)


class CookieTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get('access')
        if not token:
            return Response({'detail': 'No access token provided'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            UntypedToken(token)
        except (InvalidToken, TokenError) as e:
            return Response({'detail': 'Invalid access token'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'detail': 'Valid access token'}, status=status.HTTP_200_OK)
