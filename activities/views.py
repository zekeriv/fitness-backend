from rest_framework import generics, permissions
from .models import DailyActivity
from .serializers import DailyActivitySerializer

class DailyActivityListCreateView(generics.ListCreateAPIView):
    serializer_class = DailyActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only return activities of the logged-in user
        return DailyActivity.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Assign logged-in user automatically
        serializer.save(user=self.request.user)

class DailyActivityDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DailyActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DailyActivity.objects.filter(user=self.request.user)