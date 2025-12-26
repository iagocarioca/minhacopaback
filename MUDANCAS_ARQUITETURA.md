# Mudanças na Arquitetura - Times agora pertencem à Temporada

## 📋 Resumo

A arquitetura foi refatorada para que **times sejam fixos dentro de uma temporada**, ao invés de serem criados por rodada. Isso reflete melhor o funcionamento real de peladas onde os times são sempre os mesmos.

---

## 🔄 Arquitetura Anterior vs Nova

### ❌ ANTES (Arquitetura Antiga)
```
Temporada → Rodada → Times (criados por rodada) → Jogadores adicionados
```

**Problemas:**
- Times eram recriados a cada rodada
- Jogadores precisavam ser re-escalados toda rodada
- Perda de continuidade dos times
- Estatísticas fragmentadas por rodada

### ✅ AGORA (Nova Arquitetura)
```
Temporada → Times Fixos (com jogadores escalados)
         ↓
      Rodada → Seleciona quais times jogam → Partidas
```

**Vantagens:**
- Times são permanentes durante toda a temporada
- Jogadores já ficam escalados nos times
- Estatísticas acumuladas dos times ao longo da temporada
- Mais simples e intuitivo

---

## 🗂️ Mudanças nos Models

### Model `Time` ([models.py:103-128](source/domain/peladas/models.py#L103-L128))

**Antes:**
```python
class Time(db.Model):
    rodada_id = db.Column(db.Integer, db.ForeignKey('rodadas.id'))
    nome = db.Column(db.String(50))
    ordem = db.Column(db.Integer)
    # ...
```

**Agora:**
```python
class Time(db.Model):
    temporada_id = db.Column(db.Integer, db.ForeignKey('temporadas.id'))
    nome = db.Column(db.String(50))
    cor = db.Column(db.String(30), nullable=True)  # NOVO
    criado_em = db.Column(db.DateTime)  # NOVO
    # Campo 'ordem' foi removido
```

**Mudanças:**
- `rodada_id` → `temporada_id`
- Removido: `ordem` (não faz mais sentido ter ordem fixa)
- Adicionado: `cor` (para identificar times, ex: "azul", "vermelho")
- Adicionado: `criado_em` (timestamp de criação)

### Model `Temporada`

**Novo relacionamento:**
```python
class Temporada(db.Model):
    # ...
    times = db.relationship('Time', back_populates='temporada', lazy=True)  # NOVO
```

### Model `Rodada`

**Relacionamento removido:**
```python
class Rodada(db.Model):
    # ...
    # REMOVIDO: times = db.relationship('Time', back_populates='rodada')
```

---

## 🛠️ Mudanças nos Services

### TimeService ([services.py:446-581](source/domain/peladas/services.py#L446-L581))

#### Método `criar_time()`

**Antes:**
```python
def criar_time(rodada_id, nome, ordem):
    rodada = Rodada.query.get(rodada_id)
    novo_time = Time(rodada_id=rodada_id, nome=nome, ordem=ordem)
```

**Agora:**
```python
def criar_time(temporada_id, nome, cor=None):
    temporada = Temporada.query.get(temporada_id)
    # Valida se temporada está ativa
    novo_time = Time(temporada_id=temporada_id, nome=nome, cor=cor)
```

#### Método `listar_times_da_rodada()` → `listar_times_da_temporada()`

**Antes:**
```python
def listar_times_da_rodada(rodada_id):
    times = Time.query.filter_by(rodada_id=rodada_id).all()
```

**Agora:**
```python
def listar_times_da_temporada(temporada_id, page=1, per_page=20):
    query = Time.query.filter_by(temporada_id=temporada_id)
    # Retorna com paginação
```

#### Serialização

**Mudanças em `_serializar_time()`:**
```python
# Antes
{
    'rodada_id': time.rodada_id,
    'ordem': time.ordem
}

# Agora
{
    'temporada_id': time.temporada_id,
    'cor': time.cor,
    'criado_em': time.criado_em.isoformat()
}
```

### PartidaService ([services.py:584-615](source/domain/peladas/services.py#L584-L615))

**Validação atualizada em `criar_partida()`:**

**Antes:**
```python
# Validava se times pertenciam à rodada
if time_casa.rodada_id != rodada_id:
    return None, 'Os times devem pertencer à rodada especificada'
```

**Agora:**
```python
# Valida se times pertencem à temporada da rodada
if time_casa.temporada_id != rodada.temporada_id:
    return None, 'Os times devem pertencer à temporada da rodada'
```

### RodadaService

**`obter_rodada_por_id()` atualizado:**
- Antes: Retornava rodada com lista de times
- Agora: Retorna rodada com lista de partidas

---

## 🌐 Mudanças nas Rotas da API

### Criar Time

**Antes:**
```
POST /api/peladas/rodadas/<rodada_id>/times
Body: { "nome": "Time Azul", "ordem": 1 }
```

**Agora:**
```
POST /api/peladas/temporadas/<temporada_id>/times
Body: { "nome": "Time Azul", "cor": "azul" }
```

### Listar Times

**Antes:**
```
GET /api/peladas/rodadas/<rodada_id>/times
```

**Agora:**
```
GET /api/peladas/temporadas/<temporada_id>/times?page=1&per_page=20
```

**Resposta agora com paginação:**
```json
{
  "data": [ ...times... ],
  "meta": {
    "total": 10,
    "page": 1,
    "per_page": 20,
    "total_pages": 1,
    "has_next_page": false,
    "has_previous_page": false
  }
}
```

### Rotas que NÃO mudaram

Estas rotas continuam funcionando normalmente:
- `GET /api/peladas/times/<time_id>` - Obter time por ID
- `POST /api/peladas/times/<time_id>/jogadores` - Adicionar jogador ao time
- `DELETE /api/peladas/times/<time_id>/jogadores/<jogador_id>` - Remover jogador

---

## 💾 Mudanças no Banco de Dados

### Migration Aplicada

Arquivo: `migrations/versions/4eb396c8633e_migrar_times_de_rodada_para_temporada.py`

**O que a migration faz:**

1. **Adiciona novas colunas:**
   - `temporada_id` (INTEGER, NOT NULL, FK para temporadas.id)
   - `cor` (VARCHAR(30), NULL)
   - `criado_em` (DATETIME, NULL)

2. **Migra dados existentes:**
   ```sql
   UPDATE times t
   INNER JOIN rodadas r ON t.rodada_id = r.id
   SET t.temporada_id = r.temporada_id
   WHERE t.rodada_id IS NOT NULL
   ```

3. **Remove colunas antigas:**
   - `rodada_id` (INTEGER, FK removida)
   - `ordem` (INTEGER)

4. **Atualiza constraints:**
   - Remove FK `times_ibfk_1` (times → rodadas)
   - Adiciona FK `fk_times_temporada` (times → temporadas)

**Estrutura final da tabela `times`:**
```sql
CREATE TABLE times (
    id INT PRIMARY KEY AUTO_INCREMENT,
    temporada_id INT NOT NULL,
    nome VARCHAR(50) NOT NULL,
    cor VARCHAR(30) NULL,
    pontos INT DEFAULT 0,
    vitorias INT DEFAULT 0,
    empates INT DEFAULT 0,
    derrotas INT DEFAULT 0,
    gols_marcados INT DEFAULT 0,
    gols_sofridos INT DEFAULT 0,
    criado_em DATETIME NULL,
    FOREIGN KEY (temporada_id) REFERENCES temporadas(id)
);
```

---

## 📖 Novo Fluxo de Uso

### 1. Criar Temporada
```http
POST /api/peladas/1/temporadas
{
  "inicio_mes": "2025-01-01",
  "fim_mes": "2025-03-31"
}
```

### 2. Criar Times Fixos
```http
POST /api/peladas/temporadas/1/times
{
  "nome": "Time Azul",
  "cor": "azul"
}

POST /api/peladas/temporadas/1/times
{
  "nome": "Time Vermelho",
  "cor": "vermelho"
}
```

### 3. Escalar Jogadores nos Times
```http
POST /api/peladas/times/1/jogadores
{
  "jogador_id": 5,
  "capitao": true,
  "posicao": 1
}

POST /api/peladas/times/1/jogadores
{
  "jogador_id": 7,
  "capitao": false,
  "posicao": 2
}
```

### 4. Criar Rodada
```http
POST /api/peladas/temporadas/1/rodadas
{
  "data_rodada": "2025-01-15",
  "quantidade_times": 4,
  "jogadores_por_time": 6
}
```

### 5. Criar Partidas (Selecionar quais times jogam)
```http
POST /api/peladas/rodadas/1/partidas
{
  "time_casa_id": 1,  // Time Azul
  "time_fora_id": 2   // Time Vermelho
}
```

### 6. Jogar e Registrar Resultados
```http
POST /api/peladas/partidas/1/iniciar

POST /api/peladas/partidas/1/gols
{
  "time_id": 1,
  "jogador_id": 5,
  "minuto": 23
}

POST /api/peladas/partidas/1/finalizar
```

---

## ✅ Compatibilidade com Dados Existentes

A migration **preserva todos os dados existentes**:

- Times antigos são automaticamente migrados para suas respectivas temporadas
- Estatísticas (pontos, vitórias, gols) são mantidas
- Partidas continuam funcionando normalmente
- Relacionamento com jogadores (TimeJogador) permanece intacto

---

## 🚀 Próximos Passos Recomendados

1. ✅ **Migration aplicada** - Banco de dados atualizado
2. ⏳ **Atualizar documentação da API** - Refletir as novas rotas
3. ⏳ **Atualizar frontend** - Ajustar chamadas à API
4. ⏳ **Testar fluxo completo** - Criar temporada → times → rodadas → partidas

---

## 📝 Notas Importantes

### Para Desenvolvedores Frontend

- **Mudar chamadas de API:**
  - `/rodadas/:id/times` → `/temporadas/:id/times`

- **Atualizar payloads:**
  - Remover `ordem` ao criar time
  - Adicionar `cor` (opcional)

- **Times agora são listados com paginação**

### Para Testes

- Garantir que times criados em uma temporada permanecem disponíveis em todas as rodadas
- Validar que estatísticas acumulam corretamente ao longo das rodadas
- Testar remoção/adição de jogadores em times fixos

---

**Data da Mudança:** 2025-12-23
**Migration:** `4eb396c8633e_migrar_times_de_rodada_para_temporada.py`
**Status:** ✅ Concluído e aplicado ao banco de dados
