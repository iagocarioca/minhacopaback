# Documentação de Rotas - efootbool

Base URL: `http://localhost:5000`

**Observações gerais**:
- Prefixos registrados no app: ` /api/usuarios` (blueprint `user_bp`), ` /api/peladas` (blueprint `pelada_bp`).
- A maioria das rotas exige autenticação JWT (`Authorization: Bearer <access_token>`), exceto `POST /api/usuarios/registrar` e `POST /api/usuarios/login`.

---

## Rotas de Usuários

- **Registrar**: `POST /api/usuarios/registrar`
  - Auth: não
  - Body JSON:
    - `username` (string, obrigatório)
    - `email` (string, obrigatório)
    - `password` (string, obrigatório)
  - Sucesso: `201`
    - Exemplo:
      ```json
      { "mensagem": "Usuário criado com sucesso", "usuario": {"id": 1, "username": "joao", "email": "a@b.com"} }
      ```
  - Erros: `400`, `409`

- **Login**: `POST /api/usuarios/login`
  - Auth: não
  - Body JSON:
    - `username` (string, obrigatório)
    - `password` (string, obrigatório)
  - Sucesso: `200`
    - Exemplo (retorna tokens):
      ```json
      { "mensagem": "Login realizado com sucesso", "access_token": "...", "refresh_token": "..." }
      ```
  - Erros: `400`, `401`

- **Obter usuário atual**: `GET /api/usuarios/me`
  - Auth: sim (Bearer)
  - Query: nenhuma
  - Sucesso: `200`
    - Exemplo:
      ```json
      { "usuario": {"id":1, "username":"joao", "email":"a@b.com"} }
      ```

- **Refresh token**: `POST /api/usuarios/refresh`
  - Auth: sim (refresh token)
  - Sucesso: `200` (novo access token)

- **Atualizar usuário**: `PUT /api/usuarios/atualizar/{usuario_id}`
  - Auth: sim
  - Path param: `usuario_id` (int)
  - Body JSON: qualquer campo de perfil aceito pelo serviço (ex.: `nome`, `telefone`, `apelido`)
  - Sucesso: `200`

- **Obter usuário por id**: `GET /api/usuarios/{usuario_id}`
  - Auth: sim
  - Sucesso: `200`

- **Listar usuários**: `GET /api/usuarios/listar`
  - Auth: sim (apenas admin conforme código)
  - Query params:
    - `page` (int, opcional)
    - `per_page` (int, opcional)
  - Sucesso: `200` (paginado)

---

## Rotas de Peladas (prefixo `/api/peladas`)

- **Criar pelada**: `POST /api/peladas/`
  - Auth: sim
  - Body JSON:
    - `nome` (string, obrigatório)
    - `cidade` (string, obrigatório)
    - `fuso_horario` (string, opcional, default `America/Sao_Paulo`)
  - Sucesso: `201` com objeto `pelada` criado

- **Listar peladas**: `GET /api/peladas/`
  - Auth: sim
  - Query params: `page`, `per_page`, `usuario_id` (filtra peladas do usuário), `ativa` (true/false)
  - Sucesso: `200` (lista/paginada)

- **Obter pelada**: `GET /api/peladas/{pelada_id}`
  - Auth: sim
  - Path param: `pelada_id` (int)

- **Perfil da pelada**: `GET /api/peladas/{pelada_id}/perfil`
  - Auth: sim
  - Retorna perfil completo (gerente, jogadores, temporadas, estatísticas)

- **Atualizar pelada**: `PUT /api/peladas/{pelada_id}`
  - Auth: sim
  - Body JSON: campos aceitos pelo serviço

-- Rotas de jogadores dentro de uma pelada --

- **Criar jogador**: `POST /api/peladas/{pelada_id}/jogadores`
  - Auth: sim
  - Body JSON: `nome_completo` (obrigatório), `apelido`, `telefone`
  - Sucesso: `201`

- **Listar jogadores**: `GET /api/peladas/{pelada_id}/jogadores`
  - Auth: sim
  - Query params: `page`, `per_page`, `ativo`

- **Obter jogador**: `GET /api/peladas/jogadores/{jogador_id}`
  - Auth: sim

- **Atualizar jogador**: `PUT /api/peladas/jogadores/{jogador_id}`
  - Auth: sim
  - Body JSON: campos de perfil do jogador

-- Rotas de temporadas --

- **Criar temporada**: `POST /api/peladas/{pelada_id}/temporadas`
  - Auth: sim
  - Body JSON: `inicio_mes`, `fim_mes` (ambos obrigatórios)
  - Sucesso: `201`

- **Listar temporadas**: `GET /api/peladas/{pelada_id}/temporadas`
  - Auth: sim
  - Query params: `page`, `per_page`

- **Obter temporada**: `GET /api/peladas/temporadas/{temporada_id}`

- **Encerrar temporada**: `POST /api/peladas/temporadas/{temporada_id}/encerrar`
  - Auth: sim

-- Rotas de rodadas --

- **Criar rodada**: `POST /api/peladas/temporadas/{temporada_id}/rodadas`
  - Auth: sim
  - Body JSON: `data_rodada` (string/ISO), `quantidade_times` (int), `jogadores_por_time` (int)

- **Listar rodadas**: `GET /api/peladas/temporadas/{temporada_id}/rodadas`

- **Obter rodada**: `GET /api/peladas/rodadas/{rodada_id}`

-- Rotas de times --

- **Criar time**: `POST /api/peladas/rodadas/{rodada_id}/times`
  - Auth: sim
  - Body JSON: `nome` (string), `ordem` (int)

- **Listar times da rodada**: `GET /api/peladas/rodadas/{rodada_id}/times`

- **Obter time**: `GET /api/peladas/times/{time_id}`

- **Adicionar jogador ao time**: `POST /api/peladas/times/{time_id}/jogadores`
  - Body JSON: `jogador_id` (int, obrigatório), `capitao` (bool, opcional), `posicao` (string, opcional)

- **Remover jogador do time**: `DELETE /api/peladas/times/{time_id}/jogadores/{jogador_id}`

-- Rotas de partidas --

- **Criar partida**: `POST /api/peladas/rodadas/{rodada_id}/partidas`
  - Body JSON: `time_casa_id`, `time_fora_id` (ambos int, obrigatórios)

- **Listar partidas**: `GET /api/peladas/rodadas/{rodada_id}/partidas`

- **Obter partida**: `GET /api/peladas/partidas/{partida_id}`

- **Iniciar partida**: `POST /api/peladas/partidas/{partida_id}/iniciar`

- **Finalizar partida**: `POST /api/peladas/partidas/{partida_id}/finalizar`

-- Rotas de gols --

- **Registrar gol**: `POST /api/peladas/partidas/{partida_id}/gols`
  - Body JSON: `time_id` (int), `jogador_id` (int), `minuto` (int, opcional), `gol_contra` (bool, opcional), `assistencia_id` (int, opcional)

- **Remover gol**: `DELETE /api/peladas/gols/{gol_id}`

-- Rotas de rankings --

- **Ranking de times**: `GET /api/peladas/temporadas/{temporada_id}/ranking/times`
- **Ranking de artilheiros**: `GET /api/peladas/temporadas/{temporada_id}/ranking/artilheiros` (query `limit` opcional)
- **Ranking de assistências**: `GET /api/peladas/temporadas/{temporada_id}/ranking/assistencias` (query `limit` opcional)

-- Rotas de votações --

- **Criar votação**: `POST /api/peladas/rodadas/{rodada_id}/votacoes`
  - Body JSON: `abre_em`, `fecha_em`, `tipo` (todos obrigatórios)

- **Registrar voto**: `POST /api/peladas/votacoes/{votacao_id}/votar`
  - Body JSON: `jogador_votante_id`, `jogador_votado_id`, `pontos`

---

## Arquivos
- Especificação OpenAPI: [docs/openapi.yaml](docs/openapi.yaml)

---

Se quiser, eu gero exemplos de requisições cURL para cada rota ou amplio os schemas do OpenAPI para incluir todos os campos do modelo.
