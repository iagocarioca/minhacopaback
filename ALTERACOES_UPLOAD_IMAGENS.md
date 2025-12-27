# 📸 Alterações: Upload de Imagens para Jogadores e Times

## 🆕 Novidades Implementadas

### 1. **Upload de Foto para Jogadores**
- Jogadores agora podem ter uma foto de perfil
- Campo `foto_url` adicionado ao modelo Jogador
- Rotas de criar/atualizar jogador aceitam upload de imagem

### 2. **Upload de Escudo para Times**
- Times agora podem ter um escudo
- Campo `escudo_url` adicionado ao modelo Time
- Rotas de criar time aceitam upload de escudo

### 3. **Retorno de Imagens em Todas as Rotas GET**
- Todas as rotas que retornam jogadores agora incluem `foto_url`
- Todas as rotas que retornam times agora incluem `escudo_url`

---

## 🔄 Rotas Alteradas

### **JOGADORES**

#### `POST /api/peladas/<pelada_id>/jogadores`
**NOVO:** Aceita `multipart/form-data` com campo `foto`

**Formato (FormData):**
```
nome_completo: "João Silva" (obrigatório)
apelido: "João" (opcional)
telefone: "11999999999" (opcional)
foto: [arquivo de imagem] (opcional)
```

**Resposta:**
```json
{
  "mensagem": "Jogador criado com sucesso",
  "jogador": {
    "id": 1,
    "nome_completo": "João Silva",
    "apelido": "João",
    "telefone": "11999999999",
    "foto_url": "/static/uploads/jogadores/foto_20251225_121609_123456.jpg",
    "ativo": true,
    "pelada_id": 1,
    "criado_em": "2025-12-25T12:16:09"
  }
}
```

#### `PUT /api/peladas/jogadores/<jogador_id>`
**NOVO:** Aceita `multipart/form-data` com campo `foto`

**Formato (FormData):**
```
nome_completo: "João Silva" (opcional)
apelido: "João" (opcional)
telefone: "11999999999" (opcional)
ativo: "true" (opcional)
foto: [arquivo de imagem] (opcional)
```

**Resposta:** Mesmo formato do POST, com `foto_url` atualizado se nova foto foi enviada.

#### `GET /api/peladas/<pelada_id>/jogadores`
**ATUALIZADO:** Agora retorna `foto_url` em cada jogador

**Resposta:**
```json
{
  "data": [
    {
      "id": 1,
      "nome_completo": "João Silva",
      "apelido": "João",
      "telefone": "11999999999",
      "foto_url": "/static/uploads/jogadores/foto_20251225_121609_123456.jpg",
      "ativo": true,
      "pelada_id": 1,
      "criado_em": "2025-12-25T12:16:09"
    }
  ],
  "meta": { ... }
}
```

#### `GET /api/peladas/jogadores/<jogador_id>`
**ATUALIZADO:** Agora retorna `foto_url`

#### `GET /api/peladas/rodadas/<rodada_id>/jogadores`
**ATUALIZADO:** Agora retorna `foto_url` em cada jogador E `time_escudo_url` do time

**Resposta:**
```json
{
  "jogadores": [
    {
      "id": 1,
      "nome_completo": "João Silva",
      "apelido": "João",
      "foto_url": "/static/uploads/jogadores/foto_20251225_121609_123456.jpg",
      "posicao": "Goleiro",
      "time_id": 10,
      "time_nome": "Time Azul",
      "time_escudo_url": "/static/uploads/times/escudo_20251225_121609_789012.jpg"
    }
  ]
}
```

#### `GET /api/peladas/<pelada_id>/perfil`
**ATUALIZADO:** Agora retorna `foto_url` em cada jogador da lista

---

### **TIMES**

#### `POST /api/peladas/temporadas/<temporada_id>/times`
**NOVO:** Aceita `multipart/form-data` com campo `escudo`

**Formato (FormData):**
```
nome: "Time Azul" (obrigatório)
cor: "azul" (opcional)
escudo: [arquivo de imagem] (opcional)
```

**Resposta:**
```json
{
  "mensagem": "Time criado com sucesso",
  "time": {
    "id": 10,
    "nome": "Time Azul",
    "cor": "azul",
    "escudo_url": "/static/uploads/times/escudo_20251225_121609_789012.jpg",
    "temporada_id": 1,
    "pontos": 0,
    "vitorias": 0,
    "empates": 0,
    "derrotas": 0,
    "gols_marcados": 0,
    "gols_sofridos": 0,
    "saldo_gols": 0,
    "criado_em": "2025-12-25T12:16:09"
  }
}
```

#### `GET /api/peladas/temporadas/<temporada_id>/times`
**ATUALIZADO:** Agora retorna `escudo_url` em cada time

**Resposta:**
```json
{
  "data": [
    {
      "id": 10,
      "nome": "Time Azul",
      "cor": "azul",
      "escudo_url": "/static/uploads/times/escudo_20251225_121609_789012.jpg",
      "temporada_id": 1,
      "pontos": 0,
      ...
    }
  ],
  "meta": { ... }
}
```

#### `PUT /api/peladas/times/<time_id>`
**NOVO:** Aceita `multipart/form-data` com campo `escudo` para atualizar time

**Formato (FormData):**
```
nome: "Time Azul" (opcional)
cor: "azul" (opcional)
escudo: [arquivo de imagem] (opcional)
```

**Resposta:**
```json
{
  "mensagem": "Time atualizado com sucesso",
  "time": {
    "id": 10,
    "nome": "Time Azul",
    "cor": "azul",
    "escudo_url": "/static/uploads/times/escudo_20251225_121609_789012.jpg",
    "jogadores": [...],
    ...
  }
}
```

#### `GET /api/peladas/times/<time_id>`
**ATUALIZADO:** Agora retorna `escudo_url` no time E `foto_url` em cada jogador

**Resposta:**
```json
{
  "time": {
    "id": 10,
    "nome": "Time Azul",
    "cor": "azul",
    "escudo_url": "/static/uploads/times/escudo_20251225_121609_789012.jpg",
    "jogadores": [
      {
        "id": 1,
        "nome_completo": "João Silva",
        "apelido": "João",
        "telefone": "11999999999",
        "foto_url": "/static/uploads/jogadores/foto_20251225_121609_123456.jpg",
        "capitao": false,
        "posicao": "Goleiro"
      }
    ],
    ...
  }
}
```

#### `GET /api/peladas/temporadas/<temporada_id>/ranking/times`
**ATUALIZADO:** Agora retorna `escudo_url` em cada time do ranking

**Resposta:**
```json
{
  "ranking": [
    {
      "posicao": 1,
      "time": {
        "id": 10,
        "nome": "Time Azul",
        "cor": "azul",
        "escudo_url": "/static/uploads/times/escudo_20251225_121609_789012.jpg",
        "pontos": 15,
        ...
      }
    }
  ]
}
```

#### `GET /api/peladas/partidas/<partida_id>`
**ATUALIZADO:** Agora retorna `escudo_url` nos times (time_casa e time_fora) E `foto_url` nos jogadores dos gols

**Resposta:**
```json
{
  "partida": {
    "id": 1,
    "time_casa": {
      "id": 10,
      "nome": "Time Azul",
      "escudo_url": "/static/uploads/times/escudo_20251225_121609_789012.jpg",
      ...
    },
    "time_fora": {
      "id": 11,
      "nome": "Time Vermelho",
      "escudo_url": "/static/uploads/times/escudo_20251225_121610_123456.jpg",
      ...
    },
    "gols": [
      {
        "id": 1,
        "jogador": {
          "id": 1,
          "nome_completo": "João Silva",
          "apelido": "João",
          "foto_url": "/static/uploads/jogadores/foto_20251225_121609_123456.jpg"
        },
        "assistente": {
          "id": 2,
          "nome_completo": "Carlos Souza",
          "apelido": "Carlinhos",
          "foto_url": "/static/uploads/jogadores/foto_20251225_121610_789012.jpg"
        },
        ...
      }
    ]
  }
}
```

---

## 📁 Estrutura de Pastas de Upload

As imagens são salvas em:
- **Jogadores:** `static/uploads/jogadores/foto_YYYYMMDD_HHMMSS_microsegundos.extensao`
- **Times:** `static/uploads/times/escudo_YYYYMMDD_HHMMSS_microsegundos.extensao`
- **Peladas:** `static/uploads/peladas/logo_...` e `static/uploads/peladas/perfil_...`

---

## 🌐 URLs de Acesso

Todas as imagens são acessíveis via:
- `http://localhost:5001/static/uploads/jogadores/foto_...jpg`
- `http://localhost:5001/static/uploads/times/escudo_...jpg`
- `http://localhost:5001/static/uploads/peladas/logo_...jpg`
- `http://localhost:5001/static/uploads/peladas/perfil_...jpg`

---

## 📝 Formatos Aceitos

- **Extensões:** PNG, JPG, JPEG, GIF, WEBP
- **Content-Type:** `multipart/form-data` (para upload) ou `application/json` (sem imagens)

---

## ⚠️ Observações Importantes

1. **Compatibilidade:** As rotas ainda aceitam JSON (sem imagens), mas as URLs devem vir prontas no campo `foto_url` ou `escudo_url`
2. **Opcional:** Todos os uploads de imagem são opcionais
3. **Atualização:** Ao atualizar jogador/time, se não enviar nova imagem, a URL existente é mantida
4. **Retorno:** Todas as rotas GET que retornam jogadores ou times agora incluem as URLs das imagens (pode ser `null` se não houver imagem)

---

## 🔧 Exemplo de Uso no Frontend

### JavaScript/Fetch - Criar Jogador com Foto

```javascript
const formData = new FormData();
formData.append('nome_completo', 'João Silva');
formData.append('apelido', 'João');
formData.append('telefone', '11999999999');
formData.append('foto', arquivoFoto); // File object

fetch('http://localhost:5001/api/peladas/1/jogadores', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`
    // NÃO inclua Content-Type - o browser define automaticamente
  },
  body: formData
});
```

### JavaScript/Fetch - Criar Time com Escudo

```javascript
const formData = new FormData();
formData.append('nome', 'Time Azul');
formData.append('cor', 'azul');
formData.append('escudo', arquivoEscudo); // File object

fetch('http://localhost:5001/api/peladas/temporadas/1/times', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`
  },
  body: formData
});
```

---

## ✅ Checklist para o Frontend

- [ ] Atualizar formulário de criar jogador para aceitar upload de foto
- [ ] Atualizar formulário de editar jogador para aceitar upload de foto
- [ ] Atualizar formulário de criar time para aceitar upload de escudo
- [ ] Exibir `foto_url` nas listagens e detalhes de jogadores
- [ ] Exibir `escudo_url` nas listagens e detalhes de times
- [ ] Exibir `time_escudo_url` na lista de jogadores da rodada
- [ ] Tratar casos onde `foto_url` ou `escudo_url` são `null` (exibir placeholder)

