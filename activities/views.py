# activities/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
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
        # Only allow users to see/update/delete their own activities
        return DailyActivity.objects.filter(user=self.request.user)

    def patch(self, request, *args, **kwargs):
        """
        Handle PATCH requests for updating the activity status.
        """
        instance = self.get_object()
        status_value = request.data.get("status")

        if status_value not in ["planned", "in progress", "completed"]:
            return Response(
                {"error": "Invalid status value. Must be 'planned', 'in progress', or 'completed'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        instance.status = status_value
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
