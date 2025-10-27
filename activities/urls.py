from django.urls import path
from .views import DailyActivityListCreateView

urlpatterns = [
    path('', DailyActivityListCreateView.as_view(), name='daily_activities'),
]
