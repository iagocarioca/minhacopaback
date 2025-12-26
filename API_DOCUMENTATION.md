# EFootBool - Documentação Completa da API

> Sistema de gerenciamento de peladas de futebol com controle de jogadores, temporadas, rodadas, times, partidas, gols e rankings.

**Base URL:** `http://localhost:5001`
**Autenticação:** JWT Bearer Token (incluir no header: `Authorization: Bearer <token>`)
**Banco de Dados:** MySQL (efootbool)

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Autenticação](#autenticação)
3. [Usuários](#usuários)
4. [Peladas](#peladas)
5. [Jogadores](#jogadores)
6. [Temporadas](#temporadas)
7. [Rodadas](#rodadas)
8. [Times](#times)
9. [Partidas](#partidas)
10. [Gols](#gols)
11. [Rankings](#rankings)
12. [Votações](#votações)
13. [Modelos de Dados](#modelos-de-dados)
14. [Códigos de Status HTTP](#códigos-de-status-http)
15. [Exemplos de Integração](#exemplos-de-integração)

---

## 🎯 Visão Geral

### O que é o EFootBool?

EFootBool é uma API REST completa para gerenciar peladas de futebol amador. Permite:

- **Gerenciamento de Peladas**: Criar e administrar grupos de futebol
- **Controle de Jogadores**: Cadastro de participantes com informações completas
- **Temporadas**: Organizar períodos de competição (mensal, trimestral, etc.)
- **Rodadas**: Agendar e gerenciar datas de jogo
- **Times**: Montar escalações e times equilibrados
- **Partidas**: Controlar início, fim e placar de jogos
- **Gols**: Registrar marcadores e assistências
- **Rankings**: Acompanhar artilheiros, assistências e classificação de times
- **Votações**: Sistema de votação para melhor jogador, craque da rodada, etc.

### Sistema de Pontuação

- **Vitória**: 3 pontos
- **Empate**: 1 ponto
- **Derrota**: 0 pontos

### Critérios de Desempate

1. Número de pontos
2. Saldo de gols
3. Gols marcados

---

## 🔐 Autenticação

Todas as rotas, exceto `/api/usuarios/registrar` e `/api/usuarios/login`, requerem autenticação JWT.

### Registrar Novo Usuário

**Endpoint:** `POST /api/usuarios/registrar`
**Autenticação:** Não requerida

**Body:**
```json
{
  "username": "joao_silva",
  "email": "joao@email.com",
  "password": "senha123"
}
```

**Resposta (201):**
```json
{
  "mensagem": "Usuário criado com sucesso",
  "usuario": {
    "id": 1,
    "username": "joao_silva",
    "email": "joao@email.com",
    "status": "ativo",
    "tipo_usuario": "organizador",
    "created_at": "2025-01-20T10:30:00",
    "updated_at": "2025-01-20T10:30:00"
  }
}
```

**Erros:**
- `400`: Dados inválidos ou faltando
- `409`: Email ou username já existe

---

### Login

**Endpoint:** `POST /api/usuarios/login`
**Autenticação:** Não requerida

**Body:**
```json
{
  "username": "joao_silva",
  "password": "senha123"
}
```

**Resposta (200):**
```json
{
  "mensagem": "Login realizado com sucesso",
  "token_acesso": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_atualizacao": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "usuario": {
    "id": 1,
    "username": "joao_silva",
    "email": "joao@email.com",
    "status": "ativo",
    "tipo_usuario": "organizador",
    "created_at": "2025-01-20T10:30:00",
    "updated_at": "2025-01-20T10:30:00"
  }
}
```

**Notas:**
- `token_acesso`: expira em 1 hora
- `token_atualizacao`: expira em 30 dias

**Erros:**
- `401`: Credenciais inválidas

---

### Atualizar Token de Acesso

**Endpoint:** `POST /api/usuarios/refresh`
**Autenticação:** JWT Refresh Token

**Header:**
```
Authorization: Bearer <refresh_token>
```

**Resposta (200):**
```json
{
  "token_acesso": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### Obter Usuário Atual

**Endpoint:** `GET /api/usuarios/me`
**Autenticação:** Requerida

**Resposta (200):**
```json
{
  "usuario": {
    "id": 1,
    "username": "joao_silva",
    "email": "joao@email.com",
    "status": "ativo",
    "tipo_usuario": "organizador",
    "created_at": "2025-01-20T10:30:00",
    "updated_at": "2025-01-20T10:30:00"
  }
}
```

---

## 👥 Usuários

### Listar Todos os Usuários

**Endpoint:** `GET /api/usuarios/listar`
**Autenticação:** Requerida

**Query Params:**
- `page` (opcional, padrão: 1)
- `per_page` (opcional, padrão: 10, máximo: 100)

**Exemplo:** `GET /api/usuarios/listar?page=1&per_page=10`

**Resposta (200):**
```json
{
  "data": [
    {
      "id": 1,
      "username": "joao_silva",
      "email": "joao@email.com",
      "status": "ativo",
      "tipo_usuario": "organizador",
      "created_at": "2025-01-20T10:30:00",
      "updated_at": "2025-01-20T10:30:00"
    }
  ],
  "meta": {
    "total": 25,
    "page": 1,
    "per_page": 10,
    "total_pages": 3,
    "has_next_page": true,
    "has_previous_page": false
  }
}
```

---

### Obter Usuário por ID

**Endpoint:** `GET /api/usuarios/<usuario_id>`
**Autenticação:** Requerida

**Exemplo:** `GET /api/usuarios/1`

**Resposta (200):**
```json
{
  "usuario": {
    "id": 1,
    "username": "joao_silva",
    "email": "joao@email.com",
    "status": "ativo",
    "tipo_usuario": "organizador",
    "created_at": "2025-01-20T10:30:00",
    "updated_at": "2025-01-20T10:30:00"
  }
}
```

---

## ⚽ Peladas

### Criar Pelada

**Endpoint:** `POST /api/peladas/`
**Autenticação:** Requerida

**Body:**
```json
{
  "nome": "Pelada do Fim de Semana",
  "cidade": "São Paulo",
  "fuso_horario": "America/Sao_Paulo"
}
```

**Campos:**
- `nome` (obrigatório): Nome da pelada
- `cidade` (obrigatório): Cidade onde acontece
- `fuso_horario` (opcional, padrão: "America/Sao_Paulo"): Timezone

**Resposta (201):**
```json
{
  "mensagem": "Pelada criada com sucesso",
  "pelada": {
    "id": 1,
    "nome": "Pelada do Fim de Semana",
    "cidade": "São Paulo",
    "fuso_horario": "America/Sao_Paulo",
    "ativa": true,
    "usuario_gerente_id": 1,
    "criado_em": "2025-01-20T10:30:00"
  }
}
```

**Notas:**
- O usuário autenticado se torna automaticamente o gerente da pelada

---

### Listar Peladas

**Endpoint:** `GET /api/peladas/`
**Autenticação:** Requerida

**Query Params:**
- `page` (opcional, padrão: 1)
- `per_page` (opcional, padrão: 10)
- `usuario_id` (opcional): Filtrar por gerente
- `ativa` (opcional): true/false

**Exemplo:** `GET /api/peladas/?page=1&per_page=10&ativa=true`

**Resposta (200):**
```json
{
  "data": [
    {
      "id": 1,
      "nome": "Pelada do Fim de Semana",
      "cidade": "São Paulo",
      "fuso_horario": "America/Sao_Paulo",
      "ativa": true,
      "usuario_gerente_id": 1,
      "criado_em": "2025-01-20T10:30:00"
    }
  ],
  "meta": {
    "total": 5,
    "page": 1,
    "per_page": 10,
    "total_pages": 1,
    "has_next_page": false,
    "has_previous_page": false
  }
}
```

---

### Obter Pelada por ID

**Endpoint:** `GET /api/peladas/<pelada_id>`
**Autenticação:** Requerida

**Exemplo:** `GET /api/peladas/1`

**Resposta (200):**
```json
{
  "pelada": {
    "id": 1,
    "nome": "Pelada do Fim de Semana",
    "cidade": "São Paulo",
    "fuso_horario": "America/Sao_Paulo",
    "ativa": true,
    "usuario_gerente_id": 1,
    "criado_em": "2025-01-20T10:30:00"
  }
}
```

---

### Obter Perfil Completo da Pelada

**Endpoint:** `GET /api/peladas/<pelada_id>/perfil`
**Autenticação:** Requerida

Retorna visão completa com estatísticas, jogadores, temporadas e mais.

**Exemplo:** `GET /api/peladas/1/perfil`

**Resposta (200):**
```json
{
  "pelada": {
    "id": 1,
    "nome": "Pelada do Fim de Semana",
    "cidade": "São Paulo",
    "fuso_horario": "America/Sao_Paulo",
    "ativa": true,
    "criado_em": "2025-01-20T10:30:00"
  },
  "gerente": {
    "id": 1,
    "username": "joao_silva",
    "email": "joao@email.com"
  },
  "estatisticas": {
    "total_jogadores": 25,
    "total_temporadas": 3,
    "rodadas_realizadas": 8,
    "partidas_realizadas": 24
  },
  "jogadores": [
    {
      "id": 1,
      "nome_completo": "Carlos Silva",
      "apelido": "Carlão",
      "telefone": "(11) 99999-9999",
      "ativo": true,
      "criado_em": "2025-01-10T14:20:00"
    }
  ],
  "temporadas": [
    {
      "id": 3,
      "inicio_mes": "2025-01-01",
      "fim_mes": "2025-01-31",
      "status": "ativa",
      "criado_em": "2025-01-01T00:00:00"
    }
  ],
  "temporada_ativa": {
    "id": 3,
    "inicio_mes": "2025-01-01",
    "fim_mes": "2025-01-31",
    "status": "ativa"
  }
}
```

---

### Atualizar Pelada

**Endpoint:** `PUT /api/peladas/<pelada_id>`
**Autenticação:** Requerida

**Body:**
```json
{
  "nome": "Pelada do Sábado",
  "cidade": "Rio de Janeiro",
  "ativa": true
}
```

**Resposta (200):**
```json
{
  "mensagem": "Pelada atualizada com sucesso",
  "pelada": {
    "id": 1,
    "nome": "Pelada do Sábado",
    "cidade": "Rio de Janeiro",
    "fuso_horario": "America/Sao_Paulo",
    "ativa": true,
    "usuario_gerente_id": 1,
    "criado_em": "2025-01-20T10:30:00"
  }
}
```

---

## 🏃 Jogadores

### Criar Jogador

**Endpoint:** `POST /api/peladas/<pelada_id>/jogadores`
**Autenticação:** Requerida

**Body:**
```json
{
  "nome_completo": "Carlos Silva",
  "apelido": "Carlão",
  "telefone": "(11) 99999-9999"
}
```

**Campos:**
- `nome_completo` (obrigatório): Nome completo do jogador
- `apelido` (opcional): Apelido
- `telefone` (opcional): Telefone de contato

**Resposta (201):**
```json
{
  "mensagem": "Jogador criado com sucesso",
  "jogador": {
    "id": 1,
    "pelada_id": 1,
    "nome_completo": "Carlos Silva",
    "apelido": "Carlão",
    "telefone": "(11) 99999-9999",
    "ativo": true,
    "criado_em": "2025-01-20T10:30:00"
  }
}
```

---

### Listar Jogadores da Pelada

**Endpoint:** `GET /api/peladas/<pelada_id>/jogadores`
**Autenticação:** Requerida

**Query Params:**
- `page` (opcional, padrão: 1)
- `per_page` (opcional, padrão: 50)
- `ativo` (opcional): true/false

**Exemplo:** `GET /api/peladas/1/jogadores?page=1&ativo=true`

**Resposta (200):**
```json
{
  "data": [
    {
      "id": 1,
      "pelada_id": 1,
      "nome_completo": "Carlos Silva",
      "apelido": "Carlão",
      "telefone": "(11) 99999-9999",
      "ativo": true,
      "criado_em": "2025-01-20T10:30:00"
    }
  ],
  "meta": {
    "total": 25,
    "page": 1,
    "per_page": 50,
    "total_pages": 1,
    "has_next_page": false,
    "has_previous_page": false
  }
}
```

---

### Obter Jogador por ID

**Endpoint:** `GET /api/peladas/jogadores/<jogador_id>`
**Autenticação:** Requerida

**Resposta (200):**
```json
{
  "jogador": {
    "id": 1,
    "pelada_id": 1,
    "nome_completo": "Carlos Silva",
    "apelido": "Carlão",
    "telefone": "(11) 99999-9999",
    "ativo": true,
    "criado_em": "2025-01-20T10:30:00"
  }
}
```

---

### Atualizar Jogador

**Endpoint:** `PUT /api/peladas/jogadores/<jogador_id>`
**Autenticação:** Requerida

**Body:**
```json
{
  "nome_completo": "Carlos Alberto Silva",
  "apelido": "Carlinhos",
  "telefone": "(11) 98888-8888",
  "ativo": true
}
```

**Resposta (200):**
```json
{
  "mensagem": "Jogador atualizado com sucesso",
  "jogador": {
    "id": 1,
    "pelada_id": 1,
    "nome_completo": "Carlos Alberto Silva",
    "apelido": "Carlinhos",
    "telefone": "(11) 98888-8888",
    "ativo": true,
    "criado_em": "2025-01-20T10:30:00"
  }
}
```

---

## 📅 Temporadas

### Criar Temporada

**Endpoint:** `POST /api/peladas/<pelada_id>/temporadas`
**Autenticação:** Requerida

**Body:**
```json
{
  "inicio_mes": "2025-01-01",
  "fim_mes": "2025-01-31"
}
```

**Campos:**
- `inicio_mes` (obrigatório): Data de início no formato YYYY-MM-DD
- `fim_mes` (obrigatório): Data de fim no formato YYYY-MM-DD

**Resposta (201):**
```json
{
  "mensagem": "Temporada criada com sucesso",
  "temporada": {
    "id": 1,
    "pelada_id": 1,
    "inicio_mes": "2025-01-01",
    "fim_mes": "2025-01-31",
    "status": "ativa",
    "criado_em": "2025-01-01T00:00:00"
  }
}
```

**Notas:**
- Apenas uma temporada pode estar ativa por vez
- Encerre a temporada atual antes de criar uma nova

**Erros:**
- `400`: Já existe uma temporada ativa para esta pelada

---

### Listar Temporadas da Pelada

**Endpoint:** `GET /api/peladas/<pelada_id>/temporadas`
**Autenticação:** Requerida

**Query Params:**
- `page` (opcional, padrão: 1)
- `per_page` (opcional, padrão: 10)
- `status` (opcional): ativa/encerrada

**Exemplo:** `GET /api/peladas/1/temporadas?status=ativa`

**Resposta (200):**
```json
{
  "data": [
    {
      "id": 1,
      "pelada_id": 1,
      "inicio_mes": "2025-01-01",
      "fim_mes": "2025-01-31",
      "status": "ativa",
      "criado_em": "2025-01-01T00:00:00"
    }
  ],
  "meta": {
    "total": 3,
    "page": 1,
    "per_page": 10,
    "total_pages": 1,
    "has_next_page": false,
    "has_previous_page": false
  }
}
```

---

### Obter Temporada por ID

**Endpoint:** `GET /api/peladas/temporadas/<temporada_id>`
**Autenticação:** Requerida

**Resposta (200):**
```json
{
  "temporada": {
    "id": 1,
    "pelada_id": 1,
    "inicio_mes": "2025-01-01",
    "fim_mes": "2025-01-31",
    "status": "ativa",
    "criado_em": "2025-01-01T00:00:00"
  }
}
```

---

### Encerrar Temporada

**Endpoint:** `POST /api/peladas/temporadas/<temporada_id>/encerrar`
**Autenticação:** Requerida

**Resposta (200):**
```json
{
  "mensagem": "Temporada encerrada com sucesso",
  "temporada": {
    "id": 1,
    "pelada_id": 1,
    "inicio_mes": "2025-01-01",
    "fim_mes": "2025-01-31",
    "status": "encerrada",
    "criado_em": "2025-01-01T00:00:00"
  }
}
```

---

## 🗓️ Rodadas

### Criar Rodada

**Endpoint:** `POST /api/peladas/temporadas/<temporada_id>/rodadas`
**Autenticação:** Requerida

**Body:**
```json
{
  "data_rodada": "2025-01-15",
  "quantidade_times": 4,
  "jogadores_por_time": 6
}
```

**Campos:**
- `data_rodada` (obrigatório): Data da rodada no formato YYYY-MM-DD
- `quantidade_times` (obrigatório): Quantidade de times que jogarão
- `jogadores_por_time` (obrigatório): Número de jogadores por time

**Resposta (201):**
```json
{
  "mensagem": "Rodada criada com sucesso",
  "rodada": {
    "id": 1,
    "temporada_id": 1,
    "data_rodada": "2025-01-15",
    "quantidade_times": 4,
    "jogadores_por_time": 6,
    "status": "pendente",
    "criado_em": "2025-01-10T10:00:00"
  }
}
```

---

### Listar Rodadas da Temporada

**Endpoint:** `GET /api/peladas/temporadas/<temporada_id>/rodadas`
**Autenticação:** Requerida

**Query Params:**
- `page` (opcional, padrão: 1)
- `per_page` (opcional, padrão: 10)
- `status` (opcional): pendente/em_andamento/finalizada

**Exemplo:** `GET /api/peladas/temporadas/1/rodadas?status=finalizada`

**Resposta (200):**
```json
{
  "data": [
    {
      "id": 1,
      "temporada_id": 1,
      "data_rodada": "2025-01-15",
      "quantidade_times": 4,
      "jogadores_por_time": 6,
      "status": "finalizada",
      "criado_em": "2025-01-10T10:00:00"
    }
  ],
  "meta": {
    "total": 8,
    "page": 1,
    "per_page": 10,
    "total_pages": 1,
    "has_next_page": false,
    "has_previous_page": false
  }
}
```

---

### Obter Rodada por ID

**Endpoint:** `GET /api/peladas/rodadas/<rodada_id>`
**Autenticação:** Requerida

Retorna a rodada com todos os times e jogadores escalados.

**Resposta (200):**
```json
{
  "rodada": {
    "id": 1,
    "temporada_id": 1,
    "data_rodada": "2025-01-15",
    "quantidade_times": 4,
    "jogadores_por_time": 6,
    "status": "finalizada",
    "criado_em": "2025-01-10T10:00:00",
    "times": [
      {
        "id": 1,
        "nome": "Time Azul",
        "ordem": 1,
        "pontos": 3,
        "vitorias": 1,
        "empates": 0,
        "derrotas": 0,
        "gols_marcados": 5,
        "gols_sofridos": 2,
        "saldo_gols": 3,
        "jogadores": [
          {
            "id": 5,
            "nome_completo": "João Silva",
            "apelido": "Joãozinho",
            "capitao": true,
            "posicao": 1
          }
        ]
      }
    ]
  }
}
```

---

## 👕 Times

### Criar Time

**Endpoint:** `POST /api/peladas/rodadas/<rodada_id>/times`
**Autenticação:** Requerida

**Body:**
```json
{
  "nome": "Time Azul",
  "ordem": 1
}
```

**Campos:**
- `nome` (obrigatório): Nome do time (ex: Time Azul, Time Vermelho)
- `ordem` (obrigatório): Ordem do time na rodada (1, 2, 3, 4...)

**Resposta (201):**
```json
{
  "mensagem": "Time criado com sucesso",
  "time": {
    "id": 1,
    "rodada_id": 1,
    "nome": "Time Azul",
    "ordem": 1,
    "pontos": 0,
    "vitorias": 0,
    "empates": 0,
    "derrotas": 0,
    "gols_marcados": 0,
    "gols_sofridos": 0,
    "saldo_gols": 0
  }
}
```

---

### Listar Times da Rodada

**Endpoint:** `GET /api/peladas/rodadas/<rodada_id>/times`
**Autenticação:** Requerida

**Query Params:**
- `page` (opcional, padrão: 1)
- `per_page` (opcional, padrão: 20)

**Exemplo:** `GET /api/peladas/rodadas/1/times`

**Resposta (200):**
```json
{
  "data": [
    {
      "id": 1,
      "rodada_id": 1,
      "nome": "Time Azul",
      "ordem": 1,
      "pontos": 3,
      "vitorias": 1,
      "empates": 0,
      "derrotas": 0,
      "gols_marcados": 5,
      "gols_sofridos": 2,
      "saldo_gols": 3
    },
    {
      "id": 2,
      "rodada_id": 1,
      "nome": "Time Vermelho",
      "ordem": 2,
      "pontos": 0,
      "vitorias": 0,
      "empates": 0,
      "derrotas": 1,
      "gols_marcados": 2,
      "gols_sofridos": 5,
      "saldo_gols": -3
    }
  ],
  "meta": {
    "total": 4,
    "page": 1,
    "per_page": 20,
    "total_pages": 1,
    "has_next_page": false,
    "has_previous_page": false
  }
}
```

---

### Obter Time por ID

**Endpoint:** `GET /api/peladas/times/<time_id>`
**Autenticação:** Requerida

Retorna o time com todos os jogadores escalados.

**Resposta (200):**
```json
{
  "time": {
    "id": 1,
    "rodada_id": 1,
    "nome": "Time Azul",
    "ordem": 1,
    "pontos": 3,
    "vitorias": 1,
    "empates": 0,
    "derrotas": 0,
    "gols_marcados": 5,
    "gols_sofridos": 2,
    "saldo_gols": 3,
    "jogadores": [
      {
        "id": 5,
        "nome_completo": "João Silva",
        "apelido": "Joãozinho",
        "telefone": "(11) 99999-9999",
        "capitao": true,
        "posicao": 1
      },
      {
        "id": 7,
        "nome_completo": "Pedro Santos",
        "apelido": "Pedrinho",
        "telefone": "(11) 98888-8888",
        "capitao": false,
        "posicao": 2
      }
    ]
  }
}
```

---

### Adicionar Jogador ao Time

**Endpoint:** `POST /api/peladas/times/<time_id>/jogadores`
**Autenticação:** Requerida

**Body:**
```json
{
  "jogador_id": 1,
  "capitao": true,
  "posicao": 1
}
```

**Campos:**
- `jogador_id` (obrigatório): ID do jogador a ser adicionado
- `capitao` (opcional, padrão: false): Se é capitão do time
- `posicao` (opcional): Posição na escalação (1, 2, 3...)

**Resposta (201):**
```json
{
  "message": "Jogador adicionado ao time com sucesso"
}
```

---

### Remover Jogador do Time

**Endpoint:** `DELETE /api/peladas/times/<time_id>/jogadores/<jogador_id>`
**Autenticação:** Requerida

**Resposta (200):**
```json
{
  "message": "Jogador removido do time com sucesso"
}
```

---

## 🏆 Partidas

### Criar Partida

**Endpoint:** `POST /api/peladas/rodadas/<rodada_id>/partidas`
**Autenticação:** Requerida

**Body:**
```json
{
  "time_casa_id": 1,
  "time_fora_id": 2
}
```

**Campos:**
- `time_casa_id` (obrigatório): ID do time da casa
- `time_fora_id` (obrigatório): ID do time visitante

**Resposta (201):**
```json
{
  "mensagem": "Partida criada com sucesso",
  "partida": {
    "id": 1,
    "rodada_id": 1,
    "time_casa_id": 1,
    "time_fora_id": 2,
    "inicio": null,
    "fim": null,
    "gols_casa": 0,
    "gols_fora": 0,
    "status": "agendada"
  }
}
```

---

### Listar Partidas da Rodada

**Endpoint:** `GET /api/peladas/rodadas/<rodada_id>/partidas`
**Autenticação:** Requerida

**Query Params:**
- `page` (opcional, padrão: 1)
- `per_page` (opcional, padrão: 20)
- `status` (opcional): agendada/em_andamento/finalizada

**Exemplo:** `GET /api/peladas/rodadas/1/partidas?status=finalizada`

**Resposta (200):**
```json
{
  "data": [
    {
      "id": 1,
      "rodada_id": 1,
      "time_casa_id": 1,
      "time_fora_id": 2,
      "inicio": "2025-01-15T14:00:00",
      "fim": "2025-01-15T15:00:00",
      "gols_casa": 3,
      "gols_fora": 2,
      "status": "finalizada"
    }
  ],
  "meta": {
    "total": 6,
    "page": 1,
    "per_page": 20,
    "total_pages": 1,
    "has_next_page": false,
    "has_previous_page": false
  }
}
```

---

### Obter Partida por ID

**Endpoint:** `GET /api/peladas/partidas/<partida_id>`
**Autenticação:** Requerida

Retorna a partida completa com times, estatísticas e gols.

**Resposta (200):**
```json
{
  "partida": {
    "id": 1,
    "rodada_id": 1,
    "time_casa_id": 1,
    "time_fora_id": 2,
    "inicio": "2025-01-15T14:00:00",
    "fim": "2025-01-15T15:00:00",
    "gols_casa": 3,
    "gols_fora": 2,
    "status": "finalizada",
    "time_casa": {
      "id": 1,
      "nome": "Time Azul",
      "pontos": 3,
      "vitorias": 1,
      "empates": 0,
      "derrotas": 0,
      "gols_marcados": 3,
      "gols_sofridos": 2,
      "saldo_gols": 1
    },
    "time_fora": {
      "id": 2,
      "nome": "Time Vermelho",
      "pontos": 0,
      "vitorias": 0,
      "empates": 0,
      "derrotas": 1,
      "gols_marcados": 2,
      "gols_sofridos": 3,
      "saldo_gols": -1
    },
    "gols": [
      {
        "id": 1,
        "partida_id": 1,
        "time_id": 1,
        "jogador": {
          "id": 5,
          "nome_completo": "João Silva",
          "apelido": "Joãozinho"
        },
        "assistente": {
          "id": 7,
          "nome_completo": "Pedro Oliveira",
          "apelido": "Pedrinho"
        },
        "minuto": 23,
        "gol_contra": false,
        "criado_em": "2025-01-15T14:23:00"
      }
    ]
  }
}
```

---

### Iniciar Partida

**Endpoint:** `POST /api/peladas/partidas/<partida_id>/iniciar`
**Autenticação:** Requerida

**Resposta (200):**
```json
{
  "mensagem": "Partida iniciada com sucesso",
  "partida": {
    "id": 1,
    "rodada_id": 1,
    "time_casa_id": 1,
    "time_fora_id": 2,
    "inicio": "2025-01-15T14:00:00",
    "fim": null,
    "gols_casa": 0,
    "gols_fora": 0,
    "status": "em_andamento"
  }
}
```

**Notas:**
- Altera o status de "agendada" para "em_andamento"
- Registra o horário de início

---

### Finalizar Partida

**Endpoint:** `POST /api/peladas/partidas/<partida_id>/finalizar`
**Autenticação:** Requerida

**Resposta (200):**
```json
{
  "mensagem": "Partida finalizada com sucesso",
  "partida": {
    "id": 1,
    "rodada_id": 1,
    "time_casa_id": 1,
    "time_fora_id": 2,
    "inicio": "2025-01-15T14:00:00",
    "fim": "2025-01-15T15:00:00",
    "gols_casa": 3,
    "gols_fora": 2,
    "status": "finalizada"
  }
}
```

**Notas:**
- Altera o status de "em_andamento" para "finalizada"
- Registra o horário de fim
- **Calcula automaticamente a pontuação dos times:**
  - Time vencedor recebe 3 pontos
  - Em caso de empate, cada time recebe 1 ponto
  - Time perdedor recebe 0 pontos
- Atualiza estatísticas (vitórias, empates, derrotas, gols)

---

## ⚽ Gols

### Registrar Gol

**Endpoint:** `POST /api/peladas/partidas/<partida_id>/gols`
**Autenticação:** Requerida

**Body (com assistência):**
```json
{
  "time_id": 1,
  "jogador_id": 5,
  "minuto": 23,
  "gol_contra": false,
  "assistencia_id": 7
}
```

**Body (sem assistência):**
```json
{
  "time_id": 1,
  "jogador_id": 5,
  "minuto": 45,
  "gol_contra": false
}
```

**Body (gol contra):**
```json
{
  "time_id": 1,
  "jogador_id": 8,
  "minuto": 67,
  "gol_contra": true
}
```

**Campos:**
- `time_id` (obrigatório): ID do time que fez o gol
- `jogador_id` (obrigatório): ID do jogador que marcou
- `minuto` (opcional): Minuto do gol
- `gol_contra` (opcional, padrão: false): Se foi gol contra
- `assistencia_id` (opcional): ID do jogador que deu assistência

**Resposta (201):**
```json
{
  "mensagem": "Gol registrado com sucesso",
  "gol": {
    "id": 1,
    "partida_id": 1,
    "time_id": 1,
    "jogador_id": 5,
    "minuto": 23,
    "gol_contra": false,
    "criado_em": "2025-01-15T14:23:00"
  }
}
```

**Notas:**
- Gols só podem ser registrados em partidas com status "em_andamento"
- Atualiza automaticamente os contadores de gols da partida

**Erros:**
- `400`: Partida não está em andamento

---

### Remover Gol

**Endpoint:** `DELETE /api/peladas/gols/<gol_id>`
**Autenticação:** Requerida

**Resposta (200):**
```json
{
  "mensagem": "Gol removido com sucesso"
}
```

**Notas:**
- Gols só podem ser removidos se a partida não estiver finalizada
- Atualiza automaticamente os contadores de gols da partida

**Erros:**
- `400`: Partida já finalizada

---

## 📊 Rankings

### Ranking de Times por Pontos

**Endpoint:** `GET /api/peladas/temporadas/<temporada_id>/ranking/times`
**Autenticação:** Requerida

**Resposta (200):**
```json
{
  "ranking": [
    {
      "posicao": 1,
      "time": {
        "id": 1,
        "nome": "Time Azul",
        "pontos": 9,
        "vitorias": 3,
        "empates": 0,
        "derrotas": 0,
        "gols_marcados": 12,
        "gols_sofridos": 4,
        "saldo_gols": 8
      }
    },
    {
      "posicao": 2,
      "time": {
        "id": 2,
        "nome": "Time Vermelho",
        "pontos": 6,
        "vitorias": 2,
        "empates": 0,
        "derrotas": 1,
        "gols_marcados": 8,
        "gols_sofridos": 6,
        "saldo_gols": 2
      }
    }
  ]
}
```

**Critérios de ordenação:**
1. Pontos (decrescente)
2. Saldo de gols (decrescente)
3. Gols marcados (decrescente)

---

### Ranking de Artilheiros

**Endpoint:** `GET /api/peladas/temporadas/<temporada_id>/ranking/artilheiros`
**Autenticação:** Requerida

**Query Params:**
- `limit` (opcional, padrão: 10): Quantidade de jogadores no ranking

**Exemplo:** `GET /api/peladas/temporadas/1/ranking/artilheiros?limit=10`

**Resposta (200):**
```json
{
  "ranking": [
    {
      "posicao": 1,
      "jogador": {
        "id": 5,
        "nome_completo": "João Silva",
        "apelido": "Joãozinho",
        "total_gols": 8
      }
    },
    {
      "posicao": 2,
      "jogador": {
        "id": 12,
        "nome_completo": "Carlos Santos",
        "apelido": "Carlão",
        "total_gols": 6
      }
    }
  ]
}
```

---

### Ranking de Assistências

**Endpoint:** `GET /api/peladas/temporadas/<temporada_id>/ranking/assistencias`
**Autenticação:** Requerida

**Query Params:**
- `limit` (opcional, padrão: 10): Quantidade de jogadores no ranking

**Exemplo:** `GET /api/peladas/temporadas/1/ranking/assistencias?limit=10`

**Resposta (200):**
```json
{
  "ranking": [
    {
      "posicao": 1,
      "jogador": {
        "id": 7,
        "nome_completo": "Pedro Oliveira",
        "apelido": "Pedrinho",
        "total_assistencias": 5
      }
    },
    {
      "posicao": 2,
      "jogador": {
        "id": 3,
        "nome_completo": "Lucas Ferreira",
        "apelido": "Lukinha",
        "total_assistencias": 4
      }
    }
  ]
}
```

---

## 🗳️ Votações

### Criar Votação

**Endpoint:** `POST /api/peladas/rodadas/<rodada_id>/votacoes`
**Autenticação:** Requerida

**Body:**
```json
{
  "abre_em": "2025-01-15 15:00:00",
  "fecha_em": "2025-01-16 23:59:59",
  "tipo": "melhor_jogador"
}
```

**Campos:**
- `abre_em` (obrigatório): Data/hora de abertura da votação
- `fecha_em` (obrigatório): Data/hora de fechamento da votação
- `tipo` (obrigatório): Tipo da votação (ex: melhor_jogador, artilheiro, craque_da_rodada)

**Resposta (201):**
```json
{
  "mensagem": "Votação criada com sucesso",
  "votacao": {
    "id": 1,
    "rodada_id": 1,
    "abre_em": "2025-01-15T15:00:00",
    "fecha_em": "2025-01-16T23:59:59",
    "tipo": "melhor_jogador",
    "status": "pendente"
  }
}
```

**Status possíveis:**
- `pendente`: Votação ainda não aberta
- `aberta`: Votação em andamento
- `encerrada`: Votação finalizada

---

### Registrar Voto

**Endpoint:** `POST /api/peladas/votacoes/<votacao_id>/votar`
**Autenticação:** Requerida

**Body:**
```json
{
  "jogador_votante_id": 5,
  "jogador_votado_id": 8,
  "pontos": 10
}
```

**Campos:**
- `jogador_votante_id` (obrigatório): ID do jogador que está votando
- `jogador_votado_id` (obrigatório): ID do jogador que recebe o voto
- `pontos` (obrigatório): Pontuação do voto (1-10)

**Resposta (201):**
```json
{
  "mensagem": "Voto registrado com sucesso",
  "voto": {
    "id": 1,
    "votacao_id": 1,
    "jogador_votante_id": 5,
    "jogador_votado_id": 8,
    "pontos": 10,
    "criado_em": "2025-01-15T16:00:00"
  }
}
```

**Erros:**
- `400`: Votação não está aberta
- `400`: Jogador já votou nesta votação

---

## 📦 Modelos de Dados

### User (Usuário)

```typescript
interface User {
  id: number;
  username: string;
  email: string;
  status: string;                    // "ativo", "inativo"
  tipo_usuario: string;              // "organizador", "admin"
  created_at: string;                // ISO 8601
  updated_at: string;                // ISO 8601
}
```

---

### Pelada

```typescript
interface Pelada {
  id: number;
  nome: string;
  cidade: string;
  fuso_horario: string;              // Ex: "America/Sao_Paulo"
  ativa: boolean;
  usuario_gerente_id: number;
  criado_em: string;                 // ISO 8601
}
```

---

### Jogador

```typescript
interface Jogador {
  id: number;
  pelada_id: number;
  nome_completo: string;
  apelido: string | null;
  telefone: string | null;
  ativo: boolean;
  criado_em: string;                 // ISO 8601
}
```

---

### Temporada

```typescript
interface Temporada {
  id: number;
  pelada_id: number;
  inicio_mes: string;                // YYYY-MM-DD
  fim_mes: string;                   // YYYY-MM-DD
  status: string;                    // "ativa" | "encerrada"
  criado_em: string;                 // ISO 8601
}
```

---

### Rodada

```typescript
interface Rodada {
  id: number;
  temporada_id: number;
  data_rodada: string;               // YYYY-MM-DD
  quantidade_times: number;
  jogadores_por_time: number;
  status: string;                    // "pendente" | "em_andamento" | "finalizada"
  criado_em: string;                 // ISO 8601
}
```

---

### Time

```typescript
interface Time {
  id: number;
  rodada_id: number;
  nome: string;
  ordem: number;
  pontos: number;
  vitorias: number;
  empates: number;
  derrotas: number;
  gols_marcados: number;
  gols_sofridos: number;
  saldo_gols: number;
}
```

---

### TimeJogador (Associação)

```typescript
interface TimeJogador {
  id: number;
  time_id: number;
  jogador_id: number;
  capitao: boolean;
  posicao: number | null;
}
```

---

### Partida

```typescript
interface Partida {
  id: number;
  rodada_id: number;
  time_casa_id: number;
  time_fora_id: number;
  inicio: string | null;             // ISO 8601
  fim: string | null;                // ISO 8601
  gols_casa: number;
  gols_fora: number;
  status: string;                    // "agendada" | "em_andamento" | "finalizada"
}
```

---

### Gol

```typescript
interface Gol {
  id: number;
  partida_id: number;
  time_id: number;
  jogador_id: number;
  assistencia_id: number | null;
  minuto: number | null;
  gol_contra: boolean;
  criado_em: string;                 // ISO 8601
}
```

---

### Votacao

```typescript
interface Votacao {
  id: number;
  rodada_id: number;
  abre_em: string;                   // ISO 8601
  fecha_em: string;                  // ISO 8601
  tipo: string;
  status: string;                    // "pendente" | "aberta" | "encerrada"
}
```

---

### Voto

```typescript
interface Voto {
  id: number;
  votacao_id: number;
  jogador_votante_id: number;
  jogador_votado_id: number;
  pontos: number;
  criado_em: string;                 // ISO 8601
}
```

---

### Paginação (Meta)

```typescript
interface PaginationMeta {
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
  has_next_page: boolean;
  has_previous_page: boolean;
}

interface PaginatedResponse<T> {
  data: T[];
  meta: PaginationMeta;
}
```

---

## 🔢 Códigos de Status HTTP

| Código | Descrição |
|--------|-----------|
| 200 | OK - Requisição bem-sucedida |
| 201 | Created - Recurso criado com sucesso |
| 400 | Bad Request - Dados inválidos ou faltando |
| 401 | Unauthorized - Token inválido ou ausente |
| 404 | Not Found - Recurso não encontrado |
| 409 | Conflict - Conflito (ex: usuário já existe) |
| 500 | Internal Server Error - Erro no servidor |

---

## 💻 Exemplos de Integração

### JavaScript/TypeScript (Fetch)

```typescript
// Configuração base
const API_BASE_URL = 'http://localhost:5001';
let accessToken = '';

// Login
async function login(username: string, password: string) {
  const response = await fetch(`${API_BASE_URL}/api/usuarios/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });

  const data = await response.json();
  accessToken = data.token_acesso;
  return data;
}

// Criar Pelada
async function criarPelada(nome: string, cidade: string) {
  const response = await fetch(`${API_BASE_URL}/api/peladas/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${accessToken}`
    },
    body: JSON.stringify({
      nome,
      cidade,
      fuso_horario: 'America/Sao_Paulo'
    })
  });

  return await response.json();
}

// Listar Peladas
async function listarPeladas(page = 1, perPage = 10) {
  const response = await fetch(
    `${API_BASE_URL}/api/peladas/?page=${page}&per_page=${perPage}`,
    {
      headers: { 'Authorization': `Bearer ${accessToken}` }
    }
  );

  return await response.json();
}

// Obter Perfil da Pelada
async function obterPerfilPelada(peladaId: number) {
  const response = await fetch(
    `${API_BASE_URL}/api/peladas/${peladaId}/perfil`,
    {
      headers: { 'Authorization': `Bearer ${accessToken}` }
    }
  );

  return await response.json();
}

// Criar Jogador
async function criarJogador(
  peladaId: number,
  nomeCompleto: string,
  apelido?: string
) {
  const response = await fetch(
    `${API_BASE_URL}/api/peladas/${peladaId}/jogadores`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`
      },
      body: JSON.stringify({
        nome_completo: nomeCompleto,
        apelido
      })
    }
  );

  return await response.json();
}

// Criar Temporada
async function criarTemporada(
  peladaId: number,
  inicioMes: string,
  fimMes: string
) {
  const response = await fetch(
    `${API_BASE_URL}/api/peladas/${peladaId}/temporadas`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`
      },
      body: JSON.stringify({
        inicio_mes: inicioMes,
        fim_mes: fimMes
      })
    }
  );

  return await response.json();
}

// Criar Rodada
async function criarRodada(
  temporadaId: number,
  dataRodada: string,
  quantidadeTimes: number,
  jogadoresPorTime: number
) {
  const response = await fetch(
    `${API_BASE_URL}/api/peladas/temporadas/${temporadaId}/rodadas`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`
      },
      body: JSON.stringify({
        data_rodada: dataRodada,
        quantidade_times: quantidadeTimes,
        jogadores_por_time: jogadoresPorTime
      })
    }
  );

  return await response.json();
}

// Criar Time
async function criarTime(
  rodadaId: number,
  nome: string,
  ordem: number
) {
  const response = await fetch(
    `${API_BASE_URL}/api/peladas/rodadas/${rodadaId}/times`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`
      },
      body: JSON.stringify({ nome, ordem })
    }
  );

  return await response.json();
}

// Adicionar Jogador ao Time
async function adicionarJogadorAoTime(
  timeId: number,
  jogadorId: number,
  capitao: boolean = false,
  posicao?: number
) {
  const response = await fetch(
    `${API_BASE_URL}/api/peladas/times/${timeId}/jogadores`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`
      },
      body: JSON.stringify({
        jogador_id: jogadorId,
        capitao,
        posicao
      })
    }
  );

  return await response.json();
}

// Criar Partida
async function criarPartida(
  rodadaId: number,
  timeCasaId: number,
  timeForaId: number
) {
  const response = await fetch(
    `${API_BASE_URL}/api/peladas/rodadas/${rodadaId}/partidas`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`
      },
      body: JSON.stringify({
        time_casa_id: timeCasaId,
        time_fora_id: timeForaId
      })
    }
  );

  return await response.json();
}

// Iniciar Partida
async function iniciarPartida(partidaId: number) {
  const response = await fetch(
    `${API_BASE_URL}/api/peladas/partidas/${partidaId}/iniciar`,
    {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${accessToken}` }
    }
  );

  return await response.json();
}

// Registrar Gol
async function registrarGol(
  partidaId: number,
  timeId: number,
  jogadorId: number,
  minuto?: number,
  assistenciaId?: number,
  golContra: boolean = false
) {
  const response = await fetch(
    `${API_BASE_URL}/api/peladas/partidas/${partidaId}/gols`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`
      },
      body: JSON.stringify({
        time_id: timeId,
        jogador_id: jogadorId,
        minuto,
        assistencia_id: assistenciaId,
        gol_contra: golContra
      })
    }
  );

  return await response.json();
}

// Finalizar Partida
async function finalizarPartida(partidaId: number) {
  const response = await fetch(
    `${API_BASE_URL}/api/peladas/partidas/${partidaId}/finalizar`,
    {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${accessToken}` }
    }
  );

  return await response.json();
}

// Obter Ranking de Times
async function obterRankingTimes(temporadaId: number) {
  const response = await fetch(
    `${API_BASE_URL}/api/peladas/temporadas/${temporadaId}/ranking/times`,
    {
      headers: { 'Authorization': `Bearer ${accessToken}` }
    }
  );

  return await response.json();
}

// Obter Ranking de Artilheiros
async function obterRankingArtilheiros(
  temporadaId: number,
  limit: number = 10
) {
  const response = await fetch(
    `${API_BASE_URL}/api/peladas/temporadas/${temporadaId}/ranking/artilheiros?limit=${limit}`,
    {
      headers: { 'Authorization': `Bearer ${accessToken}` }
    }
  );

  return await response.json();
}
```

---

### Axios (React/Vue/Angular)

```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5001',
  headers: { 'Content-Type': 'application/json' }
});

// Interceptor para adicionar token
api.interceptors.request.use(config => {
  const token = localStorage.getItem('accessToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Login
export const login = async (username: string, password: string) => {
  const { data } = await api.post('/api/usuarios/login', {
    username,
    password
  });
  localStorage.setItem('accessToken', data.token_acesso);
  localStorage.setItem('refreshToken', data.token_atualizacao);
  return data;
};

// Criar Pelada
export const criarPelada = async (nome: string, cidade: string) => {
  const { data } = await api.post('/api/peladas/', {
    nome,
    cidade,
    fuso_horario: 'America/Sao_Paulo'
  });
  return data;
};

// Listar Peladas
export const listarPeladas = async (page = 1, perPage = 10) => {
  const { data } = await api.get('/api/peladas/', {
    params: { page, per_page: perPage }
  });
  return data;
};

// Obter Perfil da Pelada
export const obterPerfilPelada = async (peladaId: number) => {
  const { data } = await api.get(`/api/peladas/${peladaId}/perfil`);
  return data;
};

// Criar Temporada
export const criarTemporada = async (
  peladaId: number,
  inicioMes: string,
  fimMes: string
) => {
  const { data } = await api.post(
    `/api/peladas/${peladaId}/temporadas`,
    { inicio_mes: inicioMes, fim_mes: fimMes }
  );
  return data;
};

// Criar Partida
export const criarPartida = async (
  rodadaId: number,
  timeCasaId: number,
  timeForaId: number
) => {
  const { data } = await api.post(
    `/api/peladas/rodadas/${rodadaId}/partidas`,
    { time_casa_id: timeCasaId, time_fora_id: timeForaId }
  );
  return data;
};

// Registrar Gol
export const registrarGol = async (
  partidaId: number,
  timeId: number,
  jogadorId: number,
  minuto?: number,
  assistenciaId?: number
) => {
  const { data } = await api.post(
    `/api/peladas/partidas/${partidaId}/gols`,
    {
      time_id: timeId,
      jogador_id: jogadorId,
      minuto,
      assistencia_id: assistenciaId,
      gol_contra: false
    }
  );
  return data;
};

// Obter Ranking de Times
export const obterRankingTimes = async (temporadaId: number) => {
  const { data } = await api.get(
    `/api/peladas/temporadas/${temporadaId}/ranking/times`
  );
  return data;
};
```

---

## 📌 Notas Importantes

1. **Autenticação**: Todas as rotas exceto `/registrar` e `/login` requerem JWT token
2. **Formato de Datas**: Use ISO 8601 (`YYYY-MM-DDTHH:mm:ss`) ou `YYYY-MM-DD` para datas
3. **Paginação**: Todas as listagens suportam paginação com `page` e `per_page` (máximo: 100)
4. **Fuso Horário**: Padrão é `America/Sao_Paulo` (horário de Brasília)
5. **IDs**: Todos os IDs são inteiros
6. **Booleanos**: Use `true`/`false` em JSON
7. **Tokens JWT**: Access token expira em 1 hora, Refresh token em 30 dias
8. **Base URL**: API roda na porta 5001 (não 5000)

---

## 🔄 Fluxo Típico de Uso

```
1. Registro/Login
   └─ Obter token de acesso

2. Criar Pelada
   └─ Define nome e cidade

3. Adicionar Jogadores
   └─ Cadastrar todos os participantes

4. Criar Temporada
   └─ Define período (início e fim)

5. Criar Rodada
   └─ Define data e configurações (times, jogadores/time)

6. Criar Times
   └─ Monta os times da rodada

7. Adicionar Jogadores aos Times
   └─ Escala os jogadores em cada time

8. Criar Partidas
   └─ Define confrontos (time casa vs time fora)

9. Iniciar Partida
   └─ Marca início da partida

10. Registrar Gols
    └─ Durante a partida, registrar cada gol

11. Finalizar Partida
    └─ Marca fim e calcula pontuação automaticamente

12. Consultar Rankings
    └─ Ver classificação, artilheiros e assistências

13. Criar Votação (opcional)
    └─ Para melhor jogador, craque da rodada, etc.

14. Registrar Votos
    └─ Jogadores votam

15. Repetir passos 5-14 para novas rodadas

16. Encerrar Temporada
    └─ Finalizar período de competição
```

---

## 🛠️ Suporte

Para dúvidas ou problemas, entre em contato ou abra uma issue no repositório.

---

**Versão da API:** 1.0
**Última Atualização:** 2025-12-23
