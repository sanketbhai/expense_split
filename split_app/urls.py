# urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('api/login/', LoginView.as_view(), name='token_obtain_pair'),
    path('api/simplify/', Simplify.as_view(), name='simplify'),
    path('api/expense/', Expense.as_view(), name='expense'),
    path('api/owns/', OwnsApi.as_view(), name='owns'),
    # Add other URL patterns as needed
]
