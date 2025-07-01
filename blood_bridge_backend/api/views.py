from rest_framework import generics, status
from rest_framework.response import Response
from django.utils.timezone import now
from django.utils.timesince import timesince
from django.db.models import Q, Count
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView

from .models import BloodRequest
from .serializers import BloodRequestSerializer

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authtoken.models import Token
from .models import Donor
from .serializers import DonorSerializer, DonorLoginSerializer

from rest_framework.authentication import TokenAuthentication


from rest_framework.generics import RetrieveAPIView
from .models import BloodRequest
from .serializers import BloodRequestSerializer

class BloodRequestRetrieveView(RetrieveAPIView):
    queryset = BloodRequest.objects.all()
    serializer_class = BloodRequestSerializer

class BloodRequestListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = BloodRequestSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'bloodGroup', 'contact', 'location', 'hospital', 'urgency', 'status']
    ordering_fields = ['requestedAt', 'urgency']
    ordering = ['-requestedAt']

    def get_queryset(self):
        queryset = BloodRequest.objects.filter(status='Active')
        blood_group = self.request.query_params.get('bloodGroup')
        location = self.request.query_params.get('location')

        if blood_group:
            queryset = queryset.filter(bloodGroup__iexact=blood_group)
        if location:
            queryset = queryset.filter(location__iexact=location)

        return queryset

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class BloodRequestDeleteView(APIView):
    def delete(self, request, pk):
        try:
            blood_request = BloodRequest.objects.get(pk=pk)
            blood_request.delete()
            return Response({"message": "Blood request deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except BloodRequest.DoesNotExist:
            return Response({"error": "Request not found."}, status=status.HTTP_404_NOT_FOUND)

class BloodRequestStats(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        total_requests = BloodRequest.objects.filter(status='Active').count()
        critical_requests = BloodRequest.objects.filter(status='Active', urgency='Critical').count()
        return Response({
            "total_requests": total_requests,
            "critical_requests": critical_requests
        })

class BloodRequestMarkFulfilled(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            blood_request = BloodRequest.objects.get(pk=pk)
            blood_request.status = 'Fulfilled'
            blood_request.save()

            # ✅ Update the donor's lastDonated field
            donor = request.user  # This is your logged-in Donor instance
            donor.donationCount = getattr(donor, 'donationCount', 0) + 1  # Increment donation count
            donor.lastDonated = now()
            donor.save()

            return Response({
                "message": "Blood request marked as fulfilled. Donor info updated."
            })

        except BloodRequest.DoesNotExist:
            return Response({"error": "Request not found."}, status=status.HTTP_404_NOT_FOUND)







class DonorViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['location', 'bloodGroup']

    def get_permissions(self):
        if self.action in ['create', 'login', 'list']:
            return [AllowAny()]
        return super().get_permissions()

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        serializer = DonorLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Get or create a token for the authenticated user
        token, created = Token.objects.get_or_create(user=user)

        donor_data = DonorSerializer(user).data
        return Response({
            'token': token.key,
            'donor': donor_data,
        })
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        donor = serializer.save()

        # Create token for new donor
        token, created = Token.objects.get_or_create(user=donor)

        donor_data = DonorSerializer(donor).data
        headers = self.get_success_headers(serializer.data)
        return Response({
            'token': token.key,
            'donor': donor_data,
        }, status=status.HTTP_201_CREATED, headers=headers)
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)  # this tells if it's partial update
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
