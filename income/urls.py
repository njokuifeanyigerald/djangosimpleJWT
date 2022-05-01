from django.urls import path
from .views import IncomeView, IncomeDetailView

urlpatterns = [
    path('', IncomeView.as_view(), name='income'),
    path('<int:id>/', IncomeDetailView.as_view(), name='incomeDetail'),
]
