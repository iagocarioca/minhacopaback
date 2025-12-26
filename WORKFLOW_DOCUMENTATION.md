# Fluxo de Trabalho Completo - Sistema de Peladas

## Visão Geral

Este documento descreve o fluxo completo de uso do sistema de gestão de peladas (futebol amador), desde a criação de uma pelada até o acompanhamento de rankings e estatísticas.

## Sistema de Pontuação

- **Vitória**: 3 pontos
- **Empate**: 1 ponto
- **Derrota**: 0 pontos

## Fluxo Completo do Sistema

### 1. Criação de Pelada e Jogadores

#### 1.1 Criar uma Pelada
```
POST /api/peladas/
```
**Body:**
```json
{
  "nome": "Pelada do Bairro",
  "cidade": "São Paulo",
  "fuso_horario": "America/Sao_Paulo"
}
```

#### 1.2 Adicionar Jogadores à Pelada
```
POST /api/peladas/{pelada_id}/jogadores
```
**Body:**
```json
{
  "nome_completo": "João Silva",
  "apelido": "Joãozinho",
  "telefone": "+5511999999999"
}
```

**Repita este passo para adicionar todos os jogadores que participarão da pelada.**

---

### 2. Criar Temporada

#### 2.1 Criar uma Nova Temporada
```
POST /api/peladas/{pelada_id}/temporadas
```
**Body:**
```json
{
  "inicio_mes": "2025-01-01",
  "fim_mes": "2025-03-31"
}
```

**Nota:** Apenas uma temporada pode estar ativa por vez. Encerre a temporada atual antes de criar uma nova.

---

### 3. Criar Rodada

#### 3.1 Criar uma Rodada
```
POST /api/peladas/temporadas/{temporada_id}/rodadas
```
**Body:**
```json
{
  "data_rodada": "2025-01-15",
  "quantidade_times": 4,
  "jogadores_por_time": 5
}
```

---

### 4. Montar os Times (ANTES da Rodada Começar)

#### 4.1 Criar Times para a Rodada
```
POST /api/peladas/rodadas/{rodada_id}/times
```
**Body para Time 1:**
```json
{
  "nome": "Time Azul",
  "ordem": 1
}
```

**Body para Time 2:**
```json
{
  "nome": "Time Vermelho",
  "ordem": 2
}
```

**Repita para todos os times (neste exemplo, 4 times).**

#### 4.2 Adicionar Jogadores aos Times
```
POST /api/peladas/times/{time_id}/jogadores
```
**Body:**
```json
{
  "jogador_id": 5,
  "capitao": true,
  "posicao": 1
}
```

**Repita para adicionar todos os jogadores em cada time (5 jogadores por time neste exemplo).**

#### 4.3 Editar Time (Adicionar/Remover Jogadores)

**Adicionar jogador:**
```
POST /api/peladas/times/{time_id}/jogadores
```
```json
{
  "jogador_id": 10,
  "capitao": false,
  "posicao": 6
}
```

**Remover jogador:**
```
DELETE /api/peladas/times/{time_id}/jogadores/{jogador_id}
```

#### 4.4 Verificar Times Montados
```
GET /api/peladas/rodadas/{rodada_id}/times
```

**Resposta:**
```json
{
  "times": [
    {
      "id": 1,
      "nome": "Time Azul",
      "ordem": 1,
      "pontos": 0,
      "vitorias": 0,
      "empates": 0,
      "derrotas": 0,
      "gols_marcados": 0,
      "gols_sofridos": 0,
      "saldo_gols": 0,
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
```

---

### 5. Criar e Gerenciar Partidas

#### 5.1 Criar Partidas para a Rodada
```
POST /api/peladas/rodadas/{rodada_id}/partidas
```
**Body (Partida 1: Time Azul vs Time Vermelho):**
```json
{
  "time_casa_id": 1,
  "time_fora_id": 2
}
```

**Body (Partida 2: Time Amarelo vs Time Verde):**
```json
{
  "time_casa_id": 3,
  "time_fora_id": 4
}
```

#### 5.2 Iniciar uma Partida
```
POST /api/peladas/partidas/{partida_id}/iniciar
```

**Resposta:**
```json
{
  "mensagem": "Partida iniciada com sucesso",
  "partida": {
    "id": 1,
    "rodada_id": 1,
    "time_casa_id": 1,
    "time_fora_id": 2,
    "gols_casa": 0,
    "gols_fora": 0,
    "status": "em_andamento",
    "inicio": "2025-01-15T14:00:00",
    "fim": null
  }
}
```

---

### 6. Registrar Gols Durante a Partida

#### 6.1 Registrar Gol
```
POST /api/peladas/partidas/{partida_id}/gols
```
**Body (Gol com assistência):**
```json
{
  "time_id": 1,
  "jogador_id": 5,
  "minuto": 23,
  "gol_contra": false,
  "assistencia_id": 7
}
```

**Body (Gol sem assistência):**
```json
{
  "time_id": 2,
  "jogador_id": 12,
  "minuto": 45,
  "gol_contra": false
}
```

**Body (Gol contra):**
```json
{
  "time_id": 1,
  "jogador_id": 8,
  "minuto": 67,
  "gol_contra": true
}
```

#### 6.2 Remover Gol (se necessário)
```
DELETE /api/peladas/gols/{gol_id}
```

**Nota:** Apenas gols de partidas em andamento podem ser removidos.

---

### 7. Finalizar Partida

#### 7.1 Finalizar a Partida
```
POST /api/peladas/partidas/{partida_id}/finalizar
```

**O que acontece:**
- Partida é marcada como "finalizada"
- Pontuação é calculada automaticamente:
  - Time vencedor: +3 pontos
  - Empate: +1 ponto para cada time
  - Time perdedor: 0 pontos
- Estatísticas dos times são atualizadas (vitórias, empates, derrotas, gols)

**Resposta:**
```json
{
  "mensagem": "Partida finalizada com sucesso",
  "partida": {
    "id": 1,
    "rodada_id": 1,
    "time_casa_id": 1,
    "time_fora_id": 2,
    "gols_casa": 3,
    "gols_fora": 2,
    "status": "finalizada",
    "inicio": "2025-01-15T14:00:00",
    "fim": "2025-01-15T15:30:00"
  }
}
```

---

### 8. Consultar Rankings e Estatísticas

#### 8.1 Ranking de Times por Pontos
```
GET /api/peladas/temporadas/{temporada_id}/ranking/times
```

**Resposta:**
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

**Critérios de desempate:**
1. Pontos
2. Saldo de gols
3. Gols marcados

#### 8.2 Ranking de Artilheiros
```
GET /api/peladas/temporadas/{temporada_id}/ranking/artilheiros?limit=10
```

**Resposta:**
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

#### 8.3 Ranking de Assistências
```
GET /api/peladas/temporadas/{temporada_id}/ranking/assistencias?limit=10
```

**Resposta:**
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
    }
  ]
}
```

---

### 9. Consultar Detalhes de Rodada e Partidas

#### 9.1 Ver Rodada Completa com Times
```
GET /api/peladas/rodadas/{rodada_id}
```

**Resposta:**
```json
{
  "rodada": {
    "id": 1,
    "temporada_id": 1,
    "data_rodada": "2025-01-15",
    "quantidade_times": 4,
    "jogadores_por_time": 5,
    "status": "pendente",
    "times": [
      {
        "id": 1,
        "nome": "Time Azul",
        "ordem": 1,
        "pontos": 3,
        "jogadores": [...]
      }
    ]
  }
}
```

#### 9.2 Ver Partida Completa
```
GET /api/peladas/partidas/{partida_id}
```

**Resposta:**
```json
{
  "partida": {
    "id": 1,
    "rodada_id": 1,
    "time_casa_id": 1,
    "time_fora_id": 2,
    "gols_casa": 3,
    "gols_fora": 2,
    "status": "finalizada",
    "inicio": "2025-01-15T14:00:00",
    "fim": "2025-01-15T15:30:00",
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

### 10. Encerrar Temporada

#### 10.1 Encerrar a Temporada
```
POST /api/peladas/temporadas/{temporada_id}/encerrar
```

**Resposta:**
```json
{
  "mensagem": "Temporada encerrada com sucesso",
  "temporada": {
    "id": 1,
    "pelada_id": 1,
    "inicio_mes": "2025-01-01",
    "fim_mes": "2025-03-31",
    "status": "encerrada",
    "criado_em": "2025-01-01T00:00:00"
  }
}
```

---

## Resumo do Fluxo

```
1. Criar Pelada
   ↓
2. Adicionar Jogadores
   ↓
3. Criar Temporada
   ↓
4. Criar Rodada
   ↓
5. Criar Times
   ↓
6. Adicionar Jogadores aos Times (Montar Escalação)
   ↓
7. Criar Partidas
   ↓
8. Iniciar Partida
   ↓
9. Registrar Gols (durante a partida)
   ↓
10. Finalizar Partida (cálculo automático de pontos)
   ↓
11. Consultar Rankings e Estatísticas
   ↓
12. Repetir passos 4-11 para novas rodadas
   ↓
13. Encerrar Temporada
```

---

## Endpoints Importantes de Edição

### Editar Jogador
```
PUT /api/peladas/jogadores/{jogador_id}
```
```json
{
  "nome_completo": "João Silva Santos",
  "apelido": "Joãozão",
  "telefone": "+5511988888888",
  "ativo": true
}
```

### Editar Pelada
```
PUT /api/peladas/{pelada_id}
```
```json
{
  "nome": "Pelada do Bairro - 2025",
  "cidade": "São Paulo",
  "ativa": true
}
```

---

## Notas Importantes

1. **Times devem ser montados ANTES da rodada começar** - Adicione todos os jogadores aos times antes de criar partidas

2. **Edição de Times é permitida** - Você pode adicionar ou remover jogadores de um time a qualquer momento antes das partidas começarem

3. **Gols só podem ser registrados em partidas "em_andamento"**

4. **Partidas finalizadas não podem ter gols removidos**

5. **Sistema calcula pontuação automaticamente** ao finalizar partida:
   - Vitória = 3 pontos
   - Empate = 1 ponto
   - Derrota = 0 pontos

6. **Rankings são calculados em tempo real** baseados nos dados das partidas finalizadas

7. **Apenas uma temporada ativa por pelada** - Encerre a temporada atual antes de criar uma nova

8. **Assistências são opcionais** - Você pode registrar gols sem assistência

---

## Exemplo de Código Frontend (TypeScript/React)

### Criar e Montar Times para uma Rodada

```typescript
// 1. Criar rodada
const rodada = await api.post('/api/peladas/temporadas/1/rodadas', {
  data_rodada: '2025-01-15',
  quantidade_times: 4,
  jogadores_por_time: 5
});

// 2. Criar times
const times = [];
for (let i = 1; i <= 4; i++) {
  const time = await api.post(`/api/peladas/rodadas/${rodada.id}/times`, {
    nome: `Time ${i}`,
    ordem: i
  });
  times.push(time);
}

// 3. Adicionar jogadores aos times
const jogadoresPorTime = [
  [1, 2, 3, 4, 5],    // Time 1
  [6, 7, 8, 9, 10],   // Time 2
  [11, 12, 13, 14, 15], // Time 3
  [16, 17, 18, 19, 20]  // Time 4
];

for (let i = 0; i < times.length; i++) {
  for (let j = 0; j < jogadoresPorTime[i].length; j++) {
    await api.post(`/api/peladas/times/${times[i].id}/jogadores`, {
      jogador_id: jogadoresPorTime[i][j],
      capitao: j === 0, // Primeiro jogador é capitão
      posicao: j + 1
    });
  }
}

// 4. Criar partidas
await api.post(`/api/peladas/rodadas/${rodada.id}/partidas`, {
  time_casa_id: times[0].id,
  time_fora_id: times[1].id
});

await api.post(`/api/peladas/rodadas/${rodada.id}/partidas`, {
  time_casa_id: times[2].id,
  time_fora_id: times[3].id
});
```

### Registrar Gol em Partida

```typescript
const partidaId = 1;

// Registrar gol com assistência
await api.post(`/api/peladas/partidas/${partidaId}/gols`, {
  time_id: 1,
  jogador_id: 5,
  assistencia_id: 7,
  minuto: 23,
  gol_contra: false
});

// Registrar gol sem assistência
await api.post(`/api/peladas/partidas/${partidaId}/gols`, {
  time_id: 2,
  jogador_id: 12,
  minuto: 45,
  gol_contra: false
});
```

### Consultar Rankings

```typescript
// Ranking de times
const rankingTimes = await api.get(`/api/peladas/temporadas/1/ranking/times`);

// Ranking de artilheiros (top 10)
const rankingArtilheiros = await api.get(`/api/peladas/temporadas/1/ranking/artilheiros?limit=10`);

// Ranking de assistências (top 10)
const rankingAssistencias = await api.get(`/api/peladas/temporadas/1/ranking/assistencias?limit=10`);
```
