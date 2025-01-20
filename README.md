- Criar uma marquina vitual no diretorio raiz -> python3 -m venv venv
- Criar arquivo .env no diretorio raiz (Conteúdo no corpo do e-mail)
- Subir os containers -> docker-compose up --build

##- Acesse o container django_app -> docker exec -it django_app /bin/bash
##- Aplique as migrações se necessarias dentro do container -> python manage.py makemigrations && python manage.py migrate


RODAR OS TESTES
- docker-compose run test


Consulta/Filtros de contratos:

Buscar por ID do contrato -> GET /api/v1/contratos/?id_contrato=1
Buscar por CPF do tomador -> GET /api/v1/contratos/?numero_documento=12345678900
Buscar por data de emissão (ano) -> GET /api/v1/contratos/?data_emissao__year=2025
Buscar por data de emissão (mês) -> GET /api/v1/contratos/?data_emissao__month=1 
Buscar por data de emissão (mês) -> GET /api/v1/contratos/?data_emissao=2025-01-18
Buscar por estado do tomador -> GET /api/v1/contratos/?endereco_estado=SP

Ordenar por data_emissao de forma crescente (padrão) -> /api/v1/contratos/?ordering=data_emissao
Ordenar por data_emissao de forma decrescente -> /api/v1/contratos/?ordering=-data_emissao
Ordenar por valor_desembolsado de forma crescente -> /api/v1/contratos/?ordering=valor_desembolsado
Ordenar por valor_desembolsado de forma decrescente -> /api/v1/contratos/?ordering=-valor_desembolsado

Resumo dos contratos sem filtro -> /api/v1/contratos/resumo-contratos/