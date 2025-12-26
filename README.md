# XClickPayEx

Uma plataforma de gerenciamento de produtos digitais e afiliação construída com Flask. Este projeto oferece funcionalidades completas para produtores gerenciarem seus produtos, planos de pagamento, e afiliados promoverem produtos através de links rastreados.

## O que este projeto faz?

O XClickPayEx é uma API REST que permite:

- Criação e gerenciamento de usuários com diferentes níveis de acesso (Admin, Produtor, Afiliado)
- Cadastro e gestão de produtos digitais com múltiplos planos de pagamento
- Sistema de afiliação com links rastreáveis
- Autenticação JWT com tokens de acesso e refresh
- Paginação e filtros em listagens
- Soft delete e hard delete de produtos

## Estrutura do Projeto

```
xclickpayex/
├── source/
│   ├── __init__.py                      # Factory do Flask
│   ├── api/
│   │   ├── user.py                      # Rotas de usuários
│   │   ├── produtos.py                  # Rotas de produtos
│   │   ├── cliente.py                   # Rotas de clientes
│   │   └── decorators.py                # Decoradores de autorização
│   ├── domain/
│   │   ├── users/
│   │   │   ├── models.py                # Models User e Perfil
│   │   │   └── services.py              # Lógica de negócio de usuários
│   │   ├── produtos/
│   │   │   ├── models.py                # Models Produto e PlanosProdutos
│   │   │   └── services.py              # Lógica de negócio de produtos
│   │   ├── afiliados/
│   │   │   └── models.py                # Model LinksAfiliados
│   │   └── usersclient/
│   │       └── models.py                # Models Cliente e EnderecoCliente
│   └── extensions/
│       └── extensios.py                 # SQLAlchemy, Migrate, JWT
├── config.py                            # Configurações
├── run.py                               # Ponto de entrada
└── requirements.txt                     # Dependências
```

## Instalação

### 1. Clone o repositório

```bash
git clone <seu-repositorio>
cd xclickpayex
```

### 2. Crie um ambiente virtual

```bash
python -m venv env
```

Ative o ambiente:
- Windows: `env\Scripts\activate`
- Linux/Mac: `source env/bin/activate`

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados

Crie o banco de dados MySQL (via phpMyAdmin ou linha de comando):

```sql
CREATE DATABASE xclickpayex CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Configure as variáveis de ambiente (opcional)

Edite o arquivo [config.py](config.py) ou defina variáveis de ambiente:

```bash
# MySQL
MYSQL_USER=root
MYSQL_PASSWORD=sua_senha
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=xclickpayex

# Segurança (SEMPRE mude em produção!)
SECRET_KEY=sua-chave-secreta
JWT_SECRET_KEY=sua-chave-jwt-secreta
```

### 6. Execute as migrations

```bash
flask db init
flask db migrate -m "Inicial"
flask db upgrade
```

### 7. Execute a aplicação

```bash
python run.py
```

API disponível em: `http://localhost:5000`

## Documentação da API

### Autenticação

Todas as rotas, exceto `/api/usuarios/registrar` e `/api/usuarios/login`, requerem autenticação JWT.

#### Registrar novo usuário

```http
POST /api/usuarios/registrar
Content-Type: application/json

{
  "username": "joaosilva",
  "email": "joao@example.com",
  "password": "senha_segura123"
}
```

**Resposta:**
```json
{
  "mensagem": "Usuário criado com sucesso",
  "usuario": {
    "id": 1,
    "username": "joaosilva",
    "email": "joao@example.com",
    "created_at": "2025-12-08T10:30:00"
  }
}
```

#### Login

```http
POST /api/usuarios/login
Content-Type: application/json

{
  "username": "joaosilva",
  "password": "senha_segura123"
}
```

**Resposta:**
```json
{
  "mensagem": "Login realizado com sucesso",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "joaosilva",
    "email": "joao@example.com",
    "created_at": "2025-12-08T10:30:00"
  }
}
```

#### Obter usuário atual

```http
GET /api/usuarios/me
Authorization: Bearer {access_token}
```

#### Atualizar perfil do usuário

```http
PUT /api/usuarios/atualizar/{usuario_id}
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "documento": "123.456.789-00",
  "telefone": "(11) 98765-4321",
  "endereco": "Rua Exemplo, 123",
  "nome_perfil": "João Silva Produtor",
  "descricao": "Especialista em produtos digitais"
}
```

#### Listar usuários (com paginação)

```http
GET /api/usuarios/listar?page=1&per_page=10
Authorization: Bearer {access_token}
```

**Resposta:**
```json
{
  "usuarios": [...],
  "total": 50,
  "page": 1,
  "per_page": 10,
  "total_pages": 5
}
```

#### Atualizar access token

```http
POST /api/usuarios/refresh
Authorization: Bearer {refresh_token}
```

### Produtos

#### Criar produto (apenas Produtores)

```http
POST /api/produtos/criar-produto
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "nome": "Curso de Python Avançado",
  "descricao": "Aprenda Python do zero ao avançado",
  "slug": "curso-python-avancado",
  "tipo": "curso",
  "status": "ativo",
  "comissao_padrao": 30.0,
  "dias_reembolso": 7,
  "estoque": 999,
  "planos": [
    {
      "nome": "Acesso Vitalício",
      "preco": 197.00,
      "recorrente": false,
      "moeda": "BRL",
      "max_parcelas": 12
    },
    {
      "nome": "Assinatura Mensal",
      "preco": 29.90,
      "recorrente": true,
      "periodo_cobranca": "mensal",
      "intervalo_cobranca": 1,
      "moeda": "BRL"
    }
  ]
}
```

**Resposta:**
```json
{
  "message": "Produto criado com sucesso",
  "produto": {
    "id": 1,
    "nome": "Curso de Python Avançado",
    "slug": "curso-python-avancado",
    "planos": [...]
  }
}
```

#### Listar produtos (com filtros e paginação)

```http
GET /api/produtos/listar?status=ativo&tipo=curso&page=1&per_page=10
Authorization: Bearer {access_token}
```

**Parâmetros de query:**
- `status`: ativo, inativo, rascunho
- `tipo`: curso, ebook, mentoria, etc.
- `page`: número da página (padrão: 1)
- `per_page`: itens por página (padrão: 10)

**Resposta:**
```json
{
  "produtos": [...],
  "total": 25,
  "page": 1,
  "per_page": 10,
  "total_pages": 3
}
```

#### Obter detalhes de um produto

```http
GET /api/produtos/{produto_id}
Authorization: Bearer {access_token}
```

#### Atualizar produto (apenas Produtores)

```http
PUT /api/produtos/{produto_id}
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "nome": "Curso de Python Atualizado",
  "descricao": "Nova descrição",
  "status": "ativo"
}
```

#### Deletar produto - Soft Delete (apenas Produtores)

```http
DELETE /api/produtos/{produto_id}
Authorization: Bearer {access_token}
```

Este endpoint apenas marca o produto como inativo, preservando os dados.

#### Deletar produto permanentemente - Hard Delete (apenas Admin)

```http
DELETE /api/produtos/{produto_id}/deletar-permanente
Authorization: Bearer {access_token}
```

Este endpoint remove permanentemente o produto do banco de dados.

## Tipos de Usuário e Permissões

O sistema possui três tipos de usuário com diferentes níveis de acesso:

### Admin
- Acesso total ao sistema
- Pode deletar produtos permanentemente
- Gerencia todos os usuários

### Produtor
- Pode criar, editar e deletar (soft) seus próprios produtos
- Gerencia planos de pagamento
- Define comissões para afiliados

### Afiliado
- Acessa produtos disponíveis para afiliação
- Gera links de afiliado rastreáveis
- Visualiza suas comissões

## Models e Relacionamentos

### User
- **Campos principais**: id, username, email, password_hash, tipo_usuario, status
- **Tipos**: admin, produtor, afiliado
- **Relacionamentos**:
  - Um usuário pode ter vários produtos (se for produtor)
  - Um usuário pode ter vários links de afiliado (se for afiliado)
  - Um usuário tem um perfil

### Perfil
- **Campos principais**: documento, telefone, endereco, avatar_url, nome_perfil, descricao
- **Relacionamentos**: Pertence a um usuário

### Produto
- **Campos principais**: nome, descricao, slug, tipo, status, comissao_padrao, dias_reembolso, estoque
- **Relacionamentos**:
  - Pertence a um produtor (User)
  - Tem vários planos (PlanosProdutos)
  - Pode ter vários links de afiliado

### PlanosProdutos
- **Campos principais**: nome, preco, recorrente, periodo_cobranca, max_parcelas, moeda
- **Relacionamentos**: Pertence a um produto

### LinksAfiliados
- **Campos principais**: codigo, url_destino
- **Relacionamentos**: Conecta afiliado (User) e produto

### Cliente
- **Campos principais**: email, nome_completo, telefone, origem, finger_print
- **Relacionamentos**: Pode ter vários endereços

### EnderecoCliente
- **Campos principais**: tipo, cep, rua, numero, bairro, cidade, estado, pais
- **Relacionamentos**: Pertence a um cliente

## Comandos Úteis

### Flask-Migrate

```bash
# Criar nova migration
flask db migrate -m "Descrição da mudança"

# Aplicar migrations
flask db upgrade

# Reverter última migration
flask db downgrade

# Ver histórico
flask db history
```

### Desenvolvimento

```bash
# Executar em modo debug
export FLASK_ENV=development  # Linux/Mac
set FLASK_ENV=development     # Windows

python run.py
```

## Tecnologias Utilizadas

- **Flask** - Framework web
- **SQLAlchemy** - ORM para banco de dados
- **Flask-Migrate** - Gerenciamento de migrations
- **Flask-JWT-Extended** - Autenticação JWT
- **MySQL** - Banco de dados
- **PyMySQL** - Driver MySQL para Python
- **Werkzeug** - Utilitários e hash de senhas

## Segurança

- Senhas são criptografadas usando Werkzeug
- Autenticação via JWT com tokens de acesso e refresh
- Access tokens expiram em 1 hora
- Refresh tokens expiram em 30 dias
- Controle de acesso por decoradores customizados

## Próximos Passos

- [ ] Implementar rotas de checkout
- [ ] Dashboard para afiliados com métricas
- [ ] Webhook para processar pagamentos
- [ ] Sistema de notificações
- [ ] Relatórios de vendas e comissões
- [ ] Testes automatizados
- [ ] Documentação Swagger/OpenAPI

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## Licença

Este projeto é privado e proprietário.
