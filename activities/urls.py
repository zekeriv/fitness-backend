from django.urls import path
from .views import DailyActivityListCreateView, DailyActivityDetailView

urlpatterns = [
    path('', DailyActivityListCreateView.as_view(), name='daily_activities'),
    path('<int:pk>/', DailyActivityDetailView.as_view(), name='daily_activity_detail'),
]
