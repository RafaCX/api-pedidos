# API de Pedidos

## Descrição do Projeto

Este componente faz parte do sistema "Loja Online", um projeto de e-commerce baseado em microserviços. A API de Pedidos é responsável pelo gerenciamento completo do ciclo de vida dos pedidos, incluindo criação, consulta, atualização de status e exclusão.

Desenvolvida com Python e Flask, esta API implementa uma arquitetura REST e se comunica com o frontend e armazena dados em um banco SQLite. Este projeto foi desenvolvido como parte do MVP para a disciplina de Desenvolvimento Full Stack Avançado, com foco na implementação de uma solução baseada em microserviços.

## Funcionalidades

- Criação de novos pedidos com múltiplos itens
- Listagem de todos os pedidos realizados
- Consulta de detalhes de um pedido específico
- Atualização do status de um pedido
- Exclusão de pedidos

## Tecnologias Utilizadas

- Python 3.9+
- Flask (framework web)
- Flask-OpenAPI3 (documentação de API)
- SQLAlchemy (ORM)
- SQLite (banco de dados)
- Flask-CORS (para permitir requisições cross-origin)

## Requisitos

- Python 3.9 ou superior
- pip (gerenciador de pacotes do Python)
- Ambiente virtual (recomendado)

## Instalação e Configuração

Siga os passos abaixo para configurar e executar a API de Pedidos:

1. **Clone o repositório**

```bash
git clone https://github.com/RafaCX/api-pedidos.git
cd api-pedidos
```

2. **Crie e ative um ambiente virtual**

```bash
# No Windows
python -m venv env
.\env\Scripts\activate

# No Linux/Mac
python3 -m venv env
source env/bin/activate
```

3. **Instale as dependências**

```bash
pip install -r requirements.txt
```

4. **Execute a aplicação**

```bash
flask run --host 0.0.0.0 --port 5000 --reload
```

A API estará disponível em: http://localhost:5000

A documentação interativa estará disponível em: http://localhost:5000/openapi

## Endpoints

### Pedidos

- **POST /pedido**: Cria um novo pedido
  - Corpo da requisição: Dados do cliente e itens do pedido
  - Resposta: Detalhes do pedido criado

- **GET /pedidos**: Lista todos os pedidos
  - Resposta: Lista de pedidos

- **GET /pedido**: Busca um pedido por ID
  - Parâmetro de consulta: `id` (ID do pedido)
  - Resposta: Detalhes do pedido

- **PUT /pedido**: Atualiza o status de um pedido
  - Corpo da requisição: ID do pedido e novo status
  - Resposta: Detalhes do pedido atualizado

- **DELETE /pedido**: Remove um pedido
  - Parâmetro de consulta: `id` (ID do pedido)
  - Resposta: Confirmação de remoção

## Modelos de Dados

### Pedido
- `id`: Identificador único (chave primária)
- `cliente_nome`: Nome do cliente
- `cliente_email`: Email do cliente
- `valor_total`: Valor total do pedido
- `status`: Status atual do pedido ("Criado", "Em processamento", etc.)
- `data_criacao`: Data e hora de criação do pedido
- `itens`: Relação com os itens do pedido

### Item de Pedido
- `id`: Identificador único (chave primária)
- `produto_id`: ID do produto
- `produto_nome`: Nome do produto
- `quantidade`: Quantidade do produto
- `preco_unitario`: Preço unitário do produto
- `pedido`: Chave estrangeira para o pedido relacionado

## Estrutura do Projeto

```
api-pedidos/
├── models/                # Modelos de dados
│   ├── __init__.py       # Inicialização do banco de dados
│   ├── base.py           # Classe base para modelos
│   ├── pedido.py         # Modelo de Pedido
│   └── item_pedido.py    # Modelo de Item de Pedido
├── schemas/              # Esquemas para validação
│   ├── __init__.py       # Importação de esquemas
│   ├── pedido.py         # Esquemas relacionados a pedidos
│   ├── item_pedido.py    # Esquemas relacionados a itens
│   └── error.py          # Esquemas de erros
├── app.py                # Aplicação principal
├── logger.py             # Configuração de logs
├── Dockerfile            # Configuração do Docker
└── requirements.txt      # Dependências do projeto
```

## Execução com Docker

Este projeto inclui um Dockerfile para facilitar a implantação:

1. **Construa a imagem Docker**

```bash
docker build -t api-pedidos .
```

2. **Execute o contêiner**

```bash
docker run -p 5000:5000 api-pedidos
```

A API estará disponível em: http://localhost:5000


Projeto desenvolvido como MVP para a disciplina de Desenvolvimento Full Stack Avançado.