from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from expenses.serializer import ExpenseSerializer
from .models import ExpensesModel
from rest_framework import permissions
from .permissions import IsOwner
from .pagination import CustomPageNumberPagination

class ExpenseView(ListCreateAPIView):
    serializer_class = ExpenseSerializer
    queryset = ExpensesModel.objects.all()
    permission_classes= [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def perform_create(self, serializer):
        
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

class ExpenseDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes= [permissions.IsAuthenticated, IsOwner]
    lookup_field = 'id'

    def get_queryset(self):
        return ExpensesModel.objects.filter(owner=self.request.user)

