# Django Rest Framework Personal Credit
Crie o arquivo .env no diretorio raiz (Conteúdo no corpo do e-mail)
### Subir os containers:
```sh
$ docker-compose up --build
```

## Run Tests
```sh
$ docker-compose run test
```

## Criar Contrato:
```sh
POST /api/v1/contratos/
```
### Esquema de criação de contrato
```json
{
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
            "data_vencimento": "2025-02-18"
        },
        {
            "numero_parcela": 2,
            "valor_parcela": 500.00,
            "data_vencimento": "2025-03-18"
        }
    ]
}
```
## Consulta/Filtros dos Contratos:
Buscar por ID do contrato:
```sh
GET /api/v1/contratos/?id_contrato=1
```
Buscar por CPF do tomador:
```sh
GET /api/v1/contratos/?numero_documento=12345678900
```
Buscar por data de emissão (ano):
```sh
GET /api/v1/contratos/?data_emissao__year=2025
```
Buscar por data de emissão (mês):
```sh
GET /api/v1/contratos/?data_emissao__month=1 
```
Buscar por data de emissão (mês):
```sh
GET /api/v1/contratos/?data_emissao=2025-01-18
```
Buscar por estado do tomador:
```sh
GET /api/v1/contratos/?endereco_estado=SP
```

Ordenar por data_emissao de forma crescente (padrão): 
```sh
GET /api/v1/contratos/?ordering=data_emissao
```
Ordenar por data_emissao de forma decrescente:
```sh
GET /api/v1/contratos/?ordering=-data_emissao
```
Ordenar por valor_desembolsado de forma crescente:
```sh
GET /api/v1/contratos/?ordering=valor_desembolsado
```
Ordenar por valor_desembolsado de forma decrescente:
```sh
GET /api/v1/contratos/?ordering=-valor_desembolsado
```

Resumo dos contratos sem filtro:
```sh
GET /api/v1/contratos/resumo-contratos/
```