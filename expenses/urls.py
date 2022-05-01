from django.urls import path
from .views import ExpenseView, ExpenseDetailView

urlpatterns = [
    path('', ExpenseView.as_view(), name='expense'),
    path('<int:id>/', ExpenseDetailView.as_view(), name='expenseDetail'),
]
