from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Contrato
from .serializers import ContratoSerializer
import django_filters
from django_filters import rest_framework as filters
from rest_framework import filters as rest_framework_filters
from rest_framework.decorators import action
from django.db.models import Sum, F, Avg


class ContratoFilter(filters.FilterSet):
    id_contrato = filters.NumberFilter(field_name="id_contrato", lookup_expr="exact")
    numero_documento = filters.CharFilter(
        field_name="numero_documento", lookup_expr="exact"
    )
    data_emissao = filters.DateFilter(field_name="data_emissao", lookup_expr="exact")
    data_emissao__month = filters.NumberFilter(
        field_name="data_emissao", lookup_expr="month"
    )
    data_emissao__year = filters.NumberFilter(
        field_name="data_emissao", lookup_expr="year"
    )
    endereco_estado = filters.CharFilter(
        field_name="endereco_estado", lookup_expr="exact"
    )

    class Meta:
        model = Contrato
        fields = [
            "id_contrato",
            "numero_documento",
            "data_emissao",
            "data_emissao__month",
            "data_emissao__year",
            "endereco_estado",
        ]


class ContratoViewSet(ModelViewSet):
    queryset = Contrato.objects.all()
    serializer_class = ContratoSerializer
    filter_backends = (
        filters.DjangoFilterBackend,
        rest_framework_filters.OrderingFilter,
    )
    filterset_class = ContratoFilter
    ordering_fields = ["data_emissao", "valor_desembolsado"]
    ordering = ["data_emissao"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"], url_path="resumo-contratos")
    def resumo_contratos(self, request):
        contratos = self.filter_queryset(self.get_queryset())

        valor_total_receber = contratos.aggregate(
            total_valor_a_receber=Sum(F("parcelas__valor_parcela"))
        )["total_valor_a_receber"]

        valor_total_desembolsado = contratos.aggregate(
            total_valor_desembolsado=Sum("valor_desembolsado")
        )["total_valor_desembolsado"]

        numero_total_contratos = contratos.count()

        taxa_media_contratos = contratos.aggregate(
            media_taxa_contrato=Avg("taxa_contrato")
        )["media_taxa_contrato"]

        dados_consolidados = {
            "valor_total_a_receber": valor_total_receber or 0,
            "valor_total_desembolsado": valor_total_desembolsado or 0,
            "numero_total_contratos": numero_total_contratos,
            "taxa_media_contratos": taxa_media_contratos or 0,
        }

        return Response(dados_consolidados)
