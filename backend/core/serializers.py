from rest_framework import serializers
from .models import TestModel
from .models import Contrato, Parcela


class TestModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestModel
        fields = "__all__"


class ParcelaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcela
        fields = ["numero_parcela", "valor_parcela", "data_vencimento"]


class ContratoSerializer(serializers.ModelSerializer):
    parcelas = ParcelaSerializer(many=True)

    class Meta:
        model = Contrato
        fields = [
            "id_contrato",
            "data_emissao",
            "data_nascimento_tomador",
            "valor_desembolsado",
            "numero_documento",
            "endereco_pais",
            "endereco_estado",
            "endereco_cidade",
            "numero_telefone",
            "taxa_contrato",
            "parcelas",
        ]

    def create(self, validated_data):
        parcelas_data = validated_data.pop("parcelas")
        contrato = Contrato.objects.create(**validated_data)
        for parcela_data in parcelas_data:
            Parcela.objects.create(contrato=contrato, **parcela_data)
        return contrato
