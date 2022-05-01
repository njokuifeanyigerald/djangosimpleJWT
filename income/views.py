from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from income.serializer import IncomeSerializer
from .models import IncomeModel
from rest_framework import permissions
from .permissions import IsOwner
from .pagination import CustomPageNumberPagination

class IncomeView(ListCreateAPIView):
    serializer_class = IncomeSerializer
    queryset = IncomeModel.objects.all()
    permission_classes= [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

class IncomeDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = IncomeSerializer
    permission_classes= [permissions.IsAuthenticated, IsOwner]
    lookup_field = 'id'

    def get_queryset(self):
        return IncomeModel.objects.filter(owner=self.request.user)

