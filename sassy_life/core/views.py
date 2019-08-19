from rest_flex_fields import FlexFieldsModelViewSet
from sassy_life.core import models, serializers

# Create your views here.

class ProductView(FlexFieldsModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    filterset_fields = '__all__'


class PointView(FlexFieldsModelViewSet):
    queryset = models.Point.objects.all()
    serializer_class = serializers.PointSerializer
    filterset_fields = '__all__'


class SafetyTrackerView(FlexFieldsModelViewSet):
    queryset = models.SafetyTracker.objects.all()
    serializer_class = serializers.SafetyTrackerSerializer
    filterset_fields = '__all__'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
