

# Create your views here.

from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Sum
from .models import User, Farm, Cow, Activity, MilkProduction
from .serializers import UserSerializer, FarmSerializer, CowSerializer, ActivitySerializer, MilkProductionSerializer
from .permissions import IsSuperAdmin, IsAgent, IsFarmer, IsOwnerOrSuperAdmin

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role == User.ROLE_SUPERADMIN:
            return User.objects.all()
        elif user.is_authenticated:
            return User.objects.filter(id=user.id)
        return Response({'detail': 'Authentication required'}, status=status.HTTP_403_FORBIDDEN)

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            return Response({'detail': 'Authentication required'}, status=status.HTTP_403_FORBIDDEN)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class FarmViewSet(viewsets.ModelViewSet):
    queryset = Farm.objects.all()
    serializer_class = FarmSerializer
    permission_classes = [IsSuperAdmin | IsAgent]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.role == User.ROLE_SUPERADMIN:
                return Farm.objects.all()
            elif user.role == User.ROLE_AGENT:
                return Farm.objects.filter(agent=user)
        return Response({'detail': 'Authentication required'}, status=status.HTTP_403_FORBIDDEN)

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_authenticated:
            return Response({'detail': 'Authentication required'}, status=status.HTTP_403_FORBIDDEN)
        if user.role == User.ROLE_AGENT:
            serializer.save(agent=user)
        else:
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class CowViewSet(viewsets.ModelViewSet):
    queryset = Cow.objects.all()
    serializer_class = CowSerializer
    permission_classes = [IsSuperAdmin | IsAgent | IsFarmer]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.role == User.ROLE_SUPERADMIN:
                return Cow.objects.all()
            elif user.role == User.ROLE_AGENT:
                return Cow.objects.filter(owner__farm__agent=user)
            elif user.role == User.ROLE_FARMER:
                return Cow.objects.filter(owner=user)
        return Response({'detail': 'Authentication required'}, status=status.HTTP_403_FORBIDDEN)

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_authenticated:
            return Response({'detail': 'Authentication required'}, status=status.HTTP_403_FORBIDDEN)
        if user.role == User.ROLE_FARMER:
            serializer.save(owner=user)
        else:
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsSuperAdmin | IsOwnerOrSuperAdmin]
        return super().get_permissions()

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [IsSuperAdmin | IsAgent | IsFarmer]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.role == User.ROLE_SUPERADMIN:
                return Activity.objects.all()
            elif user.role == User.ROLE_AGENT:
                return Activity.objects.filter(cow__owner__farm__agent=user)
            elif user.role == User.ROLE_FARMER:
                return Activity.objects.filter(cow__owner=user)
        return Response({'detail': 'Authentication required'}, status=status.HTTP_403_FORBIDDEN)

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            return Response({'detail': 'Authentication required'}, status=status.HTTP_403_FORBIDDEN)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class MilkProductionViewSet(viewsets.ModelViewSet):
    queryset = MilkProduction.objects.all()
    serializer_class = MilkProductionSerializer
    permission_classes = [IsSuperAdmin | IsAgent | IsFarmer]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.role == User.ROLE_SUPERADMIN:
                return MilkProduction.objects.all()
            elif user.role == User.ROLE_AGENT:
                return MilkProduction.objects.filter(cow__owner__farm__agent=user)
            elif user.role == User.ROLE_FARMER:
                return MilkProduction.objects.filter(cow__owner=user)
        return Response({'detail': 'Authentication required'}, status=status.HTTP_403_FORBIDDEN)

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            return Response({'detail': 'Authentication required'}, status=status.HTTP_403_FORBIDDEN)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class MilkReportView(viewsets.ViewSet):
    permission_classes = [IsSuperAdmin | IsAgent]

    def list(self, request):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication required'}, status=status.HTTP_403_FORBIDDEN)

        filters = {}

        if request.query_params.get('farm_id'):
            filters['cow__owner__farm_id'] = request.query_params['farm_id']

        if request.query_params.get('farmer_id'):
            filters['cow__owner_id'] = request.query_params['farmer_id']

        if request.query_params.get('start_date'):
            filters['date__gte'] = request.query_params['start_date']

        if request.query_params.get('end_date'):
            filters['date__lte'] = request.query_params['end_date']

        queryset = MilkProduction.objects.filter(**filters)
        total = queryset.aggregate(total=Sum('amount'))['total'] or 0

        return Response({'total_milk': total}, status=status.HTTP_200_OK)