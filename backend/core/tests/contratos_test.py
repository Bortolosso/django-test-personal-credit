import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from core.models import Contrato, Parcela


@pytest.mark.django_db
def test_create_contrato():
    client = APIClient()
    url = reverse("contrato-list")

    payload = {
        "data_emissao": "2025-01-18",
        "data_nascimento_tomador": "2001-09-03",
        "valor_desembolsado": 10000.00,
        "numero_documento": "12345678901",
        "endereco_pais": "Brasil",
        "endereco_estado": "SP",
        "endereco_cidade": "São Paulo",
        "numero_telefone": "+5511999999999",
        "taxa_contrato": 5.5,
        "parcelas": [
            {
                "numero_parcela": 1,
                "valor_parcela": 500.00,
                "data_vencimento": "2025-02-18",
            },
            {
                "numero_parcela": 2,
                "valor_parcela": 500.00,
                "data_vencimento": "2025-03-18",
            },
        ],
    }

    response = client.post(url, payload, format="json")

    assert response.status_code == 201

    # Verifica se o contrato foi criado
    contrato = Contrato.objects.get(numero_documento="12345678901")
    assert contrato.valor_desembolsado == 10000.00
    assert contrato.endereco_cidade == "São Paulo"

    # Verifica se as parcelas foram criadas
    parcelas = Parcela.objects.filter(contrato=contrato)
    assert parcelas.count() == 2
    assert parcelas[0].numero_parcela == 1
    assert parcelas[0].valor_parcela == 500.00
    assert str(parcelas[0].data_vencimento) == "2025-02-18"


@pytest.mark.django_db
def test_filter_contratos():
    client = APIClient()
    url = reverse("contrato-list")

    contrato1 = Contrato.objects.create(
        data_emissao="2025-01-18",
        data_nascimento_tomador="2001-09-03",
        valor_desembolsado=10000.00,
        numero_documento="12345678901",
        endereco_estado="SP",
        endereco_pais="Brasil",
        endereco_cidade="São Paulo",
        numero_telefone="+5511999999999",
        taxa_contrato=5.5,
    )

    contrato2 = Contrato.objects.create(
        data_emissao="2025-01-19",
        data_nascimento_tomador="2001-09-03",
        valor_desembolsado=20000.00,
        numero_documento="98765432100",
        endereco_estado="RJ",
        endereco_pais="Brasil",
        endereco_cidade="Rio de Janeiro",
        numero_telefone="+5521999999999",
        taxa_contrato=7.5,
    )

    parcelas_data_contrato1 = [
        {
            "numero_parcela": 1,
            "valor_parcela": 500.00,
            "data_vencimento": "2025-02-18",
            "contrato": contrato1,
        },
        {
            "numero_parcela": 2,
            "valor_parcela": 500.00,
            "data_vencimento": "2025-03-18",
            "contrato": contrato1,
        },
    ]

    # Cria as parcelas contrato 1
    for parcela_data in parcelas_data_contrato1:
        Parcela.objects.create(**parcela_data)

    parcelas_data_contrato2 = [
        {
            "numero_parcela": 1,
            "valor_parcela": 750.00,
            "data_vencimento": "2025-03-19",
            "contrato": contrato2,
        },
        {
            "numero_parcela": 2,
            "valor_parcela": 750.00,
            "data_vencimento": "2025-04-19",
            "contrato": contrato2,
        },
    ]

    # Cria as parcelas contrato 2
    for parcela_data in parcelas_data_contrato2:
        Parcela.objects.create(**parcela_data)

    # Filtra por CPF
    response = client.get(url, {"numero_documento": "12345678901"})
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["numero_documento"] == "12345678901"

    # Filtra por data de emissão
    response = client.get(url, {"data_emissao": "2025-01-18"})
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["data_emissao"] == "2025-01-18"

    # Filtra por estado
    response = client.get(url, {"endereco_estado": "SP"})
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["endereco_estado"] == "SP"


@pytest.mark.django_db
def test_ordering_contratos():
    client = APIClient()
    url = reverse("contrato-list")

    contrato1 = Contrato.objects.create(
        data_emissao="2025-01-18",
        data_nascimento_tomador="2001-09-03",
        valor_desembolsado=10000.00,
        numero_documento="12345678901",
        endereco_estado="SP",
        endereco_pais="Brasil",
        endereco_cidade="São Paulo",
        numero_telefone="+5511999999999",
        taxa_contrato=5.5,
    )

    contrato2 = Contrato.objects.create(
        data_emissao="2025-01-19",
        data_nascimento_tomador="2001-09-03",
        valor_desembolsado=20000.00,
        numero_documento="98765432100",
        endereco_estado="RJ",
        endereco_pais="Brasil",
        endereco_cidade="Rio de Janeiro",
        numero_telefone="+5521999999999",
        taxa_contrato=7.5,
    )

    contrato3 = Contrato.objects.create(
        data_emissao="2025-01-20",
        data_nascimento_tomador="2001-09-03",
        valor_desembolsado=20000.00,
        numero_documento="567890123456",
        endereco_estado="SC",
        endereco_pais="Brasil",
        endereco_cidade="Santa Catarina",
        numero_telefone="+5549999999999",
        taxa_contrato=3.5,
    )

    parcelas_data_contrato1 = [
        {
            "numero_parcela": 1,
            "valor_parcela": 500.00,
            "data_vencimento": "2025-02-18",
            "contrato": contrato1,
        },
        {
            "numero_parcela": 2,
            "valor_parcela": 500.00,
            "data_vencimento": "2025-03-18",
            "contrato": contrato1,
        },
    ]

    # Cria as parcelas contrato 1
    for parcela_data in parcelas_data_contrato1:
        Parcela.objects.create(**parcela_data)

    parcelas_data_contrato2 = [
        {
            "numero_parcela": 1,
            "valor_parcela": 750.00,
            "data_vencimento": "2025-03-19",
            "contrato": contrato2,
        },
        {
            "numero_parcela": 2,
            "valor_parcela": 750.00,
            "data_vencimento": "2025-04-19",
            "contrato": contrato2,
        },
    ]

    # Cria as parcelas contrato 2
    for parcela_data in parcelas_data_contrato2:
        Parcela.objects.create(**parcela_data)

    # Cria as parcelas contrato 3
    parcelas_data_contrato3 = [
        {
            "numero_parcela": 1,
            "valor_parcela": 350.00,
            "data_vencimento": "2025-05-19",
            "contrato": contrato3,
        },
        {
            "numero_parcela": 2,
            "valor_parcela": 350.00,
            "data_vencimento": "2025-06-19",
            "contrato": contrato3,
        },
    ]

    # Cria as parcelas contrato 2
    for parcela_data in parcelas_data_contrato3:
        Parcela.objects.create(**parcela_data)

    # Ordenar por data_emissao
    response = client.get(url, {"ordering": "data_emissao"})
    assert response.status_code == 200
    assert response.data[0]["data_emissao"] == "2025-01-18"
    assert response.data[1]["data_emissao"] == "2025-01-19"
    assert response.data[2]["data_emissao"] == "2025-01-20"

    # Ordenar por valor_desembolsado
    response = client.get(url, {"ordering": "valor_desembolsado"})
    assert response.status_code == 200
    assert response.data[0]["valor_desembolsado"] == "10000.00"
    assert response.data[1]["valor_desembolsado"] == "20000.00"
    assert response.data[2]["valor_desembolsado"] == "20000.00"

    # Ordenação decrescente por valor_desembolsado
    response = client.get(url, {"ordering": "-valor_desembolsado"})
    assert response.status_code == 200
    assert response.data[0]["valor_desembolsado"] == "20000.00"
    assert response.data[1]["valor_desembolsado"] == "20000.00"
    assert response.data[2]["valor_desembolsado"] == "10000.00"


@pytest.mark.django_db
def test_resumo_contratos_sem_filtro():
    contrato1 = Contrato.objects.create(
        data_emissao="2025-01-18",
        data_nascimento_tomador="2001-09-03",
        valor_desembolsado=10000.00,
        numero_documento="12345678901",
        endereco_pais="Brasil",
        endereco_estado="SP",
        endereco_cidade="São Paulo",
        numero_telefone="+5511999999999",
        taxa_contrato=5.5,
    )
    Parcela.objects.create(
        numero_parcela=1,
        valor_parcela=500.00,
        data_vencimento="2025-02-18",
        contrato=contrato1,
    )
    Parcela.objects.create(
        numero_parcela=2,
        valor_parcela=500.00,
        data_vencimento="2025-03-18",
        contrato=contrato1,
    )

    client = APIClient()
    url = reverse("contrato-resumo-contratos")

    response = client.get(url)
    assert response.status_code == 200
    assert response.data["valor_total_a_receber"] == 1000.00
    assert response.data["valor_total_desembolsado"] == 10000.00
    assert response.data["numero_total_contratos"] == 1
    assert response.data["taxa_media_contratos"] == 5.5


@pytest.mark.django_db
def test_resumo_contratos_com_filtro_cpf():
    contrato1 = Contrato.objects.create(
        data_emissao="2025-01-18",
        data_nascimento_tomador="2001-09-03",
        valor_desembolsado=10000.00,
        numero_documento="12345678901",
        endereco_pais="Brasil",
        endereco_estado="SP",
        endereco_cidade="São Paulo",
        numero_telefone="+5511999999999",
        taxa_contrato=5.5,
    )
    contrato2 = Contrato.objects.create(
        data_emissao="2025-01-19",
        data_nascimento_tomador="2000-05-15",
        valor_desembolsado=15000.00,
        numero_documento="98765432100",
        endereco_pais="Brasil",
        endereco_estado="SP",
        endereco_cidade="São Paulo",
        numero_telefone="+5511998888888",
        taxa_contrato=6.0,
    )
    Parcela.objects.create(
        numero_parcela=1,
        valor_parcela=600.00,
        data_vencimento="2025-02-18",
        contrato=contrato1,
    )
    Parcela.objects.create(
        numero_parcela=2,
        valor_parcela=600.00,
        data_vencimento="2025-03-18",
        contrato=contrato1,
    )
    Parcela.objects.create(
        numero_parcela=1,
        valor_parcela=800.00,
        data_vencimento="2025-02-19",
        contrato=contrato2,
    )

    client = APIClient()
    url = reverse("contrato-resumo-contratos")

    response = client.get(url, {"numero_documento": "12345678901"})  # Filtro pelo CPF
    assert response.status_code == 200
    assert response.data["valor_total_a_receber"] == 1200.00
    assert response.data["valor_total_desembolsado"] == 10000.00
    assert response.data["numero_total_contratos"] == 1
    assert response.data["taxa_media_contratos"] == 5.5


@pytest.mark.django_db
def test_resumo_contratos_com_filtro_estado():
    # Cria contratos e parcelas para testar
    contrato1 = Contrato.objects.create(
        data_emissao="2025-01-18",
        data_nascimento_tomador="2001-09-03",
        valor_desembolsado=10000.00,
        numero_documento="12345678901",
        endereco_pais="Brasil",
        endereco_estado="SP",
        endereco_cidade="São Paulo",
        numero_telefone="+5511999999999",
        taxa_contrato=5.5,
    )
    contrato2 = Contrato.objects.create(
        data_emissao="2025-01-19",
        data_nascimento_tomador="2000-05-15",
        valor_desembolsado=15000.00,
        numero_documento="98765432100",
        endereco_pais="Brasil",
        endereco_estado="RJ",
        endereco_cidade="Rio de Janeiro",
        numero_telefone="+5511998888888",
        taxa_contrato=6.0,
    )
    Parcela.objects.create(
        numero_parcela=1,
        valor_parcela=600.00,
        data_vencimento="2025-02-18",
        contrato=contrato1,
    )
    Parcela.objects.create(
        numero_parcela=2,
        valor_parcela=600.00,
        data_vencimento="2025-03-18",
        contrato=contrato1,
    )
    Parcela.objects.create(
        numero_parcela=1,
        valor_parcela=800.00,
        data_vencimento="2025-02-19",
        contrato=contrato2,
    )

    client = APIClient()
    url = reverse("contrato-resumo-contratos")

    response = client.get(url, {"endereco_estado": "SP"})  # Filtro pelo estado
    assert response.status_code == 200
    assert response.data["valor_total_a_receber"] == 1200.00
    assert response.data["valor_total_desembolsado"] == 10000.00
    assert response.data["numero_total_contratos"] == 1
    assert response.data["taxa_media_contratos"] == 5.5


@pytest.mark.django_db
def test_resumo_contratos_com_filtro_data_emissao():
    # Cria contratos e parcelas para testar
    contrato1 = Contrato.objects.create(
        data_emissao="2025-01-18",
        data_nascimento_tomador="2001-09-03",
        valor_desembolsado=10000.00,
        numero_documento="12345678901",
        endereco_pais="Brasil",
        endereco_estado="SP",
        endereco_cidade="São Paulo",
        numero_telefone="+5511999999999",
        taxa_contrato=5.5,
    )
    contrato2 = Contrato.objects.create(
        data_emissao="2025-01-19",
        data_nascimento_tomador="2000-05-15",
        valor_desembolsado=15000.00,
        numero_documento="98765432100",
        endereco_pais="Brasil",
        endereco_estado="SP",
        endereco_cidade="São Paulo",
        numero_telefone="+5511998888888",
        taxa_contrato=6.0,
    )
    Parcela.objects.create(
        numero_parcela=1,
        valor_parcela=600.00,
        data_vencimento="2025-02-18",
        contrato=contrato1,
    )
    Parcela.objects.create(
        numero_parcela=2,
        valor_parcela=600.00,
        data_vencimento="2025-03-18",
        contrato=contrato1,
    )
    Parcela.objects.create(
        numero_parcela=1,
        valor_parcela=800.00,
        data_vencimento="2025-02-19",
        contrato=contrato2,
    )

    client = APIClient()
    url = reverse("contrato-resumo-contratos")

    response = client.get(
        url, {"data_emissao": "2025-01-18"}
    )  # Filtro pela data de emissão
    assert response.status_code == 200
    assert response.data["valor_total_a_receber"] == 1200.00
    assert response.data["valor_total_desembolsado"] == 10000.00
    assert response.data["numero_total_contratos"] == 1
    assert response.data["taxa_media_contratos"] == 5.5
