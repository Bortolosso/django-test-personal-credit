from django.db import models


class TestModel(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Contrato(models.Model):
    id_contrato = models.AutoField(primary_key=True)
    data_emissao = models.DateField()
    data_nascimento_tomador = models.DateField()
    valor_desembolsado = models.DecimalField(max_digits=12, decimal_places=2)
    numero_documento = models.CharField(max_length=14)  # CPF
    endereco_pais = models.CharField(max_length=100)
    endereco_estado = models.CharField(max_length=100)
    endereco_cidade = models.CharField(max_length=100)
    numero_telefone = models.CharField(max_length=15)
    taxa_contrato = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Contrato {self.id_contrato} criado com sucesso"


class Parcela(models.Model):
    contrato = models.ForeignKey(Contrato, related_name='parcelas', on_delete=models.CASCADE)
    numero_parcela = models.PositiveIntegerField()
    valor_parcela = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()

    def __str__(self):
        return f"Parcela {self.numero_parcela} - Contrato {self.contrato.id_contrato}"
