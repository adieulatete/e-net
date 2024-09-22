from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg
from .models import NetworkNode, Product
from .serializers import NetworkNodeSerializer, ProductSerializer
from .permissions import IsActiveEmployee
from .tasks import send_qr_code_via_email


class NetworkNodeViewSet(viewsets.ModelViewSet):
    """ViewSet for managing NetworkNode instances."""
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsActiveEmployee]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    def get_queryset(self):
        user = self.request.user
        try:
            employee = user.employee
        except AttributeError:
            return NetworkNode.objects.none()

        queryset = NetworkNode.objects.filter(employees=employee)

        # Additional filters
        country = self.request.query_params.get('country')
        if country:
            queryset = queryset.filter(country=country)

        product_id = self.request.query_params.get('product_id')
        if product_id:
            queryset = queryset.filter(products__id=product_id)

        return queryset


class NetworkNodeDebtStatsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for retrieving NetworkNode instances with debt greater than the average.
    """
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsActiveEmployee]

    def get_queryset(self):
        avg_debt = NetworkNode.objects.aggregate(Avg('debt_to_supplier'))['debt_to_supplier__avg']
        if avg_debt is None:
            avg_debt = 0  # Protect against empty debt case
        return NetworkNode.objects.filter(debt_to_supplier__gt=avg_debt)


class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet for managing Product instances."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsActiveEmployee]


class QRCodeViewSet(viewsets.ViewSet):
    """ViewSet for generating QR codes for the user's network node."""
    permission_classes = [IsActiveEmployee]

    @action(detail=False, methods=['get'], url_path='')
    def generate_qr(self, request):
        """Generating a QR code for a network associated with the current user and sending it by e-mail."""
        user = request.user

        try:
            employee = user.employee
            network_node = employee.network_node
        except AttributeError:
            return Response({'error': 'Employee or NetworkNode not found for this user'}, status=status.HTTP_404_NOT_FOUND)

        contact_data = (
            f"Name: {network_node.name}\n"
            f"Email: {network_node.email}\n"
            f"Address: {network_node.street}, {network_node.city}, {network_node.country}, {network_node.house_number}"
        )

        send_qr_code_via_email.delay(contact_data, employee.email)

        return Response({'message': 'QR code will be sent to your email.'}, status=status.HTTP_200_OK)
    