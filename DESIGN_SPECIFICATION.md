# EFootBool - Especificação de Design e Interface

> Documento completo descrevendo todas as páginas, funcionalidades e fluxos da aplicação para geração de design UI/UX

---

## 📱 Visão Geral da Aplicação

**EFootBool** é uma plataforma web para gerenciar peladas de futebol amador. Permite organizar temporadas, criar times fixos, agendar rodadas, registrar partidas e acompanhar rankings em tempo real.

### Conceito Central

A aplicação funciona em uma estrutura hierárquica:

```
Pelada (Grupo de Futebol)
  └── Temporada (Período de competição - ex: "Janeiro a Março 2025")
       ├── Times Fixos (criados uma vez, permanecem toda temporada)
       │    └── Jogadores escalados em cada time
       └── Rodadas (datas de jogo)
            └── Partidas (confrontos entre os times fixos)
                 └── Gols registrados
```

### Público-Alvo

- Organizadores de peladas amadoras
- Jogadores que querem acompanhar suas estatísticas
- Grupos de amigos que jogam futebol regularmente

### Plataforma

- **Web Responsiva** (Desktop e Mobile)
- **API REST** com autenticação JWT

---

## 🎨 Identidade Visual Sugerida

### Paleta de Cores
- **Primária**: Verde #10B981 (energia, esporte, campo de futebol)
- **Secundária**: Azul Escuro #1E293B (confiança, seriedade)
- **Acento**: Laranja #F59E0B (ação, destaque)
- **Neutros**: Cinza claro #F1F5F9, Cinza médio #64748B, Preto #0F172A
- **Status**:
  - Sucesso: Verde #22C55E
  - Erro: Vermelho #EF4444
  - Aviso: Amarelo #FBBF24
  - Info: Azul #3B82F6

### Tipografia
- **Títulos**: Inter ou Poppins (Bold/SemiBold)
- **Corpo**: Inter ou Open Sans (Regular/Medium)
- **Números/Estatísticas**: Roboto Mono (para tabelas e placares)

### Estilo
- **Moderno e Clean**: Cards com bordas arredondadas, sombras suaves
- **Esportivo**: Ícones de futebol, chuteira, troféu, medalhas
- **Dados visuais**: Gráficos, barras de progresso, badges

---

## 📄 Estrutura de Páginas

### 1. **Página de Login/Registro**

#### 1.1 Tela de Login

**Elementos:**
- Logo centralizado (EFootBool)
- Formulário de login:
  - Campo: Username ou Email
  - Campo: Senha
  - Checkbox: "Lembrar-me"
  - Botão: "Entrar" (primário, destaque)
  - Link: "Esqueci minha senha"
- Divisor: "ou"
- Link: "Criar nova conta"
- Background: Imagem de campo de futebol com overlay escuro

**Funcionalidades:**
- Login com JWT
- Validação em tempo real
- Mensagens de erro claras
- Redirecionamento para dashboard após login

#### 1.2 Tela de Registro

**Elementos:**
- Logo no topo
- Formulário de cadastro:
  - Campo: Nome de usuário
  - Campo: Email
  - Campo: Senha
  - Campo: Confirmar senha
  - Indicador de força da senha
  - Checkbox: "Aceito os termos de uso"
  - Botão: "Criar conta"
- Link: "Já tenho uma conta"

**Funcionalidades:**
- Validação de email único
- Validação de username único
- Verificação de força de senha
- Criação de conta e login automático

---

### 2. **Dashboard Principal**

**Layout:**
- Sidebar (navegação principal)
- Header (título da página, notificações, perfil do usuário)
- Área de conteúdo principal

#### Sidebar - Menu de Navegação

**Itens do Menu:**
1. 🏠 **Dashboard** (página inicial)
2. ⚽ **Minhas Peladas** (lista de grupos)
3. 👥 **Jogadores** (cadastro de jogadores)
4. 📅 **Temporadas** (gestão de temporadas)
5. 🎯 **Rodadas** (agendamento de jogos)
6. 👕 **Times** (times fixos da temporada)
7. 🏆 **Partidas** (jogos e resultados)
8. 📊 **Rankings** (classificação, artilheiros)
9. ⚙️ **Configurações**
10. 🚪 **Sair**

#### Header

**Elementos:**
- Título da página atual
- Breadcrumb (navegação contextual)
- Ícone de notificações (badge com contador)
- Avatar do usuário + nome
- Dropdown do perfil:
  - Meu Perfil
  - Configurações
  - Sair

#### Conteúdo do Dashboard

**Cards de Estatísticas Gerais:**
1. **Total de Peladas** (número + ícone)
2. **Total de Jogadores** (número + ícone)
3. **Rodadas Realizadas** (número + ícone)
4. **Próxima Rodada** (data + ícone)

**Seções:**
1. **Próximas Rodadas** (lista com data, hora, local)
2. **Últimas Partidas** (placar, times, data)
3. **Artilheiros** (top 5 com foto, nome, gols)
4. **Rankings de Times** (top 5 com posição, nome, pontos)

**Gráficos/Visualizações:**
- Gráfico de linha: Evolução de gols por rodada
- Gráfico de barras: Comparação de vitórias/empates/derrotas

---

### 3. **Página: Minhas Peladas**

**Objetivo:** Listar e gerenciar grupos de futebol (peladas)

**Elementos:**
- Título: "Minhas Peladas"
- Botão: "+ Nova Pelada" (canto superior direito)
- Campo de busca: "Buscar pelada..."
- Filtros: Status (Ativa/Inativa)

**Lista de Peladas (Cards):**

Cada card mostra:
- Nome da pelada
- Descrição breve
- Localização
- Status (badge: Ativa/Inativa)
- Número de jogadores
- Número de temporadas
- Botões de ação:
  - ✏️ Editar
  - 👁️ Ver detalhes
  - 🗑️ Excluir

**Modal: Criar/Editar Pelada**

Campos:
- Nome da pelada *
- Descrição
- Localização/Endereço
- Dia da semana habitual
- Horário habitual
- Status (Ativa/Inativa)
- Botões: Cancelar | Salvar

---

### 4. **Página: Detalhes da Pelada**

**Breadcrumb:** Dashboard > Minhas Peladas > [Nome da Pelada]

**Header da Pelada:**
- Nome da pelada (grande, destaque)
- Localização (ícone de pin)
- Dia e horário habitual
- Status (badge)
- Botão: "Editar Pelada"

**Abas (Tabs):**

#### Aba 1: Visão Geral
- Card: Estatísticas gerais
  - Total de jogadores cadastrados
  - Total de temporadas
  - Total de rodadas realizadas
  - Total de partidas
- Lista: Temporadas da pelada
- Lista: Últimas rodadas

#### Aba 2: Jogadores
- Lista de todos os jogadores da pelada
- Botão: "+ Adicionar Jogador"
- Cada jogador mostra:
  - Foto/Avatar
  - Nome completo
  - Apelido
  - Posição
  - Total de gols
  - Total de assistências
  - Botões: Editar | Remover

#### Aba 3: Temporadas
- Lista de temporadas
- Botão: "+ Nova Temporada"
- Cada temporada mostra:
  - Nome (ex: "Janeiro - Março 2025")
  - Data início e fim
  - Status (Ativa/Encerrada)
  - Número de times
  - Número de rodadas
  - Botão: "Ver Temporada"

---

### 5. **Página: Jogadores**

**Objetivo:** Gerenciar cadastro de jogadores

**Elementos:**
- Título: "Jogadores"
- Botão: "+ Novo Jogador"
- Campo de busca: "Buscar jogador..."
- Filtros:
  - Pelada (dropdown)
  - Posição (Goleiro, Zagueiro, Meio-campo, Atacante)
  - Status (Ativo/Inativo)

**Tabela de Jogadores:**

Colunas:
- Foto
- Nome Completo
- Apelido
- Pelada
- Posição
- Gols (total)
- Assistências (total)
- Status
- Ações (Editar | Excluir)

**Paginação:** Botões de navegação (anterior, próximo, números de página)

**Modal: Criar/Editar Jogador**

Campos:
- Foto/Avatar (upload)
- Nome completo *
- Apelido
- Email
- Telefone
- Posição * (dropdown)
- Pelada * (dropdown)
- Observações
- Status (Ativo/Inativo)
- Botões: Cancelar | Salvar

---

### 6. **Página: Temporadas**

**Objetivo:** Criar e gerenciar períodos de competição

**Elementos:**
- Título: "Temporadas"
- Filtro: Selecionar pelada (dropdown)
- Botão: "+ Nova Temporada"

**Lista de Temporadas (Cards em grade):**

Cada card mostra:
- Nome da temporada
- Datas (DD/MM/YYYY - DD/MM/YYYY)
- Status (badge: Ativa, Encerrada)
- Estatísticas:
  - N° de times
  - N° de rodadas
  - N° de partidas
- Botão: "Ver Detalhes"

**Modal: Criar Temporada**

Campos:
- Pelada * (dropdown)
- Data de início *
- Data de fim *
- Status (Ativa/Encerrada)
- Botões: Cancelar | Criar

---

### 7. **Página: Detalhes da Temporada**

**Breadcrumb:** Dashboard > Temporadas > [Nome da Temporada]

**Header:**
- Nome da temporada
- Datas
- Status (badge)
- Botão: "Editar"

**Abas (Tabs):**

#### Aba 1: Times Fixos

**Objetivo:** Criar e gerenciar times que permanecem durante toda a temporada

**Elementos:**
- Botão: "+ Criar Time"
- Lista de times em cards

**Card de Time:**
- Nome do time
- Cor identificadora (círculo colorido)
- Estatísticas:
  - Pontos
  - Vitórias / Empates / Derrotas
  - Gols Marcados / Sofridos
  - Saldo de Gols
- Jogadores escalados (lista com avatares)
- Botões:
  - "Gerenciar Jogadores"
  - "Editar Time"
  - "Excluir Time"

**Modal: Criar/Editar Time**

Campos:
- Nome do time *
- Cor (seletor de cor)
- Botões: Cancelar | Salvar

**Modal: Gerenciar Jogadores do Time**

Elementos:
- Lista de jogadores disponíveis (lado esquerdo)
- Lista de jogadores escalados (lado direito)
- Botões de adicionar/remover entre as listas
- Para cada jogador escalado:
  - Checkbox: Capitão
  - Campo: Posição (número 1-11 ou nome)
- Botões: Cancelar | Salvar

#### Aba 2: Rodadas

- Lista de rodadas da temporada
- Botão: "+ Nova Rodada"
- Cada rodada mostra:
  - Número da rodada
  - Data
  - Status (Pendente, Em andamento, Finalizada)
  - Quantidade de partidas
  - Botão: "Ver Rodada"

#### Aba 3: Ranking de Times

**Tabela Classificação:**

Colunas:
- Posição (#)
- Time (nome + cor)
- Pontos (PTS)
- Jogos (J)
- Vitórias (V)
- Empates (E)
- Derrotas (D)
- Gols Marcados (GM)
- Gols Sofridos (GS)
- Saldo de Gols (SG)

**Destaques visuais:**
- 1º lugar: destaque dourado
- 2º lugar: destaque prata
- 3º lugar: destaque bronze
- Zona de rebaixamento (se houver): fundo vermelho claro

#### Aba 4: Artilheiros

**Lista de Artilheiros:**

Cards ou tabela mostrando:
- Posição (#)
- Foto do jogador
- Nome do jogador
- Time
- Gols
- Assistências

**Top 3 com destaque visual diferenciado**

---

### 8. **Página: Rodadas**

**Objetivo:** Agendar e gerenciar datas de jogos

**Elementos:**
- Título: "Rodadas"
- Filtro: Selecionar temporada (dropdown)
- Botão: "+ Nova Rodada"

**Visualização em Calendário ou Lista**

**Card de Rodada:**
- Data e hora
- Status (badge: Pendente, Em andamento, Finalizada)
- Quantidade de times participantes
- Jogadores por time
- Lista de partidas programadas
- Botões:
  - "Ver Detalhes"
  - "Editar"
  - "Iniciar Rodada"

**Modal: Criar/Editar Rodada**

Campos:
- Temporada * (dropdown)
- Data da rodada *
- Quantidade de times * (número)
- Jogadores por time * (número)
- Status
- Botões: Cancelar | Salvar

---

### 9. **Página: Detalhes da Rodada**

**Breadcrumb:** Dashboard > Rodadas > [Rodada #N - DD/MM/YYYY]

**Header:**
- Número da rodada e data
- Status (badge)
- Botões:
  - "Editar Rodada"
  - "Iniciar Rodada" (se pendente)
  - "Finalizar Rodada" (se em andamento)

**Seção: Partidas da Rodada**

**Botão:** "+ Criar Partida"

**Lista de Partidas (Cards):**

Cada partida mostra:
- Time Casa vs Time Fora (nomes + cores)
- Placar (se em andamento ou finalizada)
- Status (Agendada, Em andamento, Finalizada)
- Horário de início e fim
- Botões:
  - "Iniciar Partida"
  - "Ver Detalhes"
  - "Finalizar Partida"

**Modal: Criar Partida**

Campos:
- Rodada (pré-selecionada)
- Time Casa * (dropdown com times da temporada)
- Time Fora * (dropdown com times da temporada)
- Botões: Cancelar | Criar Partida

---

### 10. **Página: Detalhes da Partida**

**Breadcrumb:** Dashboard > Rodadas > Rodada #N > Partida

**Header da Partida:**
- Time Casa (grande, à esquerda)
  - Nome
  - Cor
  - Logo/Shield
- **PLACAR** (centro, bem destacado)
  - Gols Casa **3 x 2** Gols Fora
- Time Fora (grande, à direita)
  - Nome
  - Cor
  - Logo/Shield
- Status da partida (badge)
- Horários: Início e Fim

**Botões de Ação:**
- "Iniciar Partida" (se agendada)
- "Registrar Gol" (se em andamento)
- "Finalizar Partida" (se em andamento)
- "Editar" (ícone)

**Seção: Gols da Partida**

**Timeline de gols (cronológica):**

Cada gol mostra:
- Minuto (ou timestamp)
- Time que marcou (com cor)
- Nome do jogador que marcou
- Nome do assistente (se houver)
- Badge: "Gol Contra" (se aplicável)
- Botão: Remover gol (ícone lixeira)

**Modal: Registrar Gol**

Campos:
- Time * (dropdown: Casa ou Fora)
- Jogador que marcou * (dropdown com jogadores do time selecionado)
- Minuto (opcional)
- Gol contra? (checkbox)
- Assistência de (dropdown com jogadores, opcional)
- Botões: Cancelar | Registrar

**Seção: Escalações**

Mostrar lado a lado:
- Escalação Time Casa
- Escalação Time Fora

Cada escalação mostra:
- Lista de jogadores com:
  - Número/Posição
  - Nome
  - Badge "Capitão" (se aplicável)

---

### 11. **Página: Times (da Temporada)**

**Objetivo:** Visualizar times fixos criados na temporada

**Elementos:**
- Título: "Times da Temporada"
- Filtro: Selecionar temporada (dropdown)
- Botão: "+ Criar Time"

**Grid de Cards de Times:**

Cada card:
- Nome do time (grande)
- Cor identificadora (barra lateral ou fundo)
- Estatísticas:
  - 🏆 Pontos: X
  - ✅ Vitórias: X
  - 🤝 Empates: X
  - ❌ Derrotas: X
  - ⚽ Gols Marcados: X
  - 🥅 Gols Sofridos: X
  - 📊 Saldo: +X ou -X
- Botão: "Ver Time"

---

### 12. **Página: Detalhes do Time**

**Breadcrumb:** Dashboard > Times > [Nome do Time]

**Header:**
- Nome do time (grande)
- Cor do time (visual destacado)
- Temporada
- Estatísticas em cards:
  - Pontos
  - Posição no ranking
  - Partidas jogadas
  - Vitórias/Empates/Derrotas
  - Gols Marcados/Sofridos/Saldo

**Abas:**

#### Aba 1: Elenco

**Lista de Jogadores do Time:**

Tabela ou cards:
- Foto
- Nome
- Posição
- É Capitão? (badge)
- Gols pelo time
- Assistências pelo time
- Botão: "Remover do time"

**Botão:** "+ Adicionar Jogador"

#### Aba 2: Partidas

**Lista de todas as partidas do time:**

Cada partida:
- Data
- Adversário
- Placar (Time X x Y Adversário)
- Resultado (badge: Vitória, Empate, Derrota)
- Botão: "Ver Partida"

#### Aba 3: Estatísticas

**Gráficos e métricas:**
- Gráfico de pizza: Vitórias vs Empates vs Derrotas
- Gráfico de barras: Gols por partida
- Média de gols marcados por jogo
- Média de gols sofridos por jogo
- Melhor artilheiro do time
- Jogador com mais assistências

---

### 13. **Página: Rankings**

**Objetivo:** Visualizar estatísticas e classificações gerais

**Elementos:**
- Título: "Rankings"
- Filtro: Selecionar temporada (dropdown)

**Abas:**

#### Aba 1: Classificação de Times

(igual à descrita na Temporada > Ranking de Times)

#### Aba 2: Artilheiros

**Ranking de gols:**

Tabela/Cards:
- Posição (#)
- Foto do jogador
- Nome
- Time atual
- Total de gols
- Total de assistências
- Média de gols por jogo

**Destaque para Top 3**

#### Aba 3: Assistências

**Ranking de assistências:**

Tabela/Cards:
- Posição (#)
- Foto do jogador
- Nome
- Time atual
- Total de assistências
- Total de gols (secundário)

**Destaque para Top 3**

#### Aba 4: Estatísticas Gerais

Cards com métricas:
- Jogador com mais gols em uma única partida
- Partida com mais gols
- Time com melhor ataque
- Time com melhor defesa
- Maior goleada
- Artilheiro da temporada

---

### 14. **Página: Votações**

**Objetivo:** Sistema de votação para melhor jogador, craque, etc.

**Elementos:**
- Título: "Votações"
- Filtro: Selecionar rodada (dropdown)
- Botão: "+ Nova Votação"

**Lista de Votações:**

Cada votação mostra:
- Título da votação (ex: "Craque da Rodada #5")
- Rodada associada
- Status (Aberta, Encerrada)
- Data limite
- Total de votos
- Botão: "Ver Resultados" ou "Votar"

**Modal: Criar Votação**

Campos:
- Título da votação *
- Rodada * (dropdown)
- Data limite *
- Botões: Cancelar | Criar

**Página/Modal: Votar**

Elementos:
- Título da votação
- Lista de candidatos (jogadores da rodada)
- Radio buttons ou cards clicáveis
- Botão: "Enviar Voto"

**Página: Resultados da Votação**

Elementos:
- Título da votação
- Status (badge)
- Gráfico de barras ou lista com:
  - Foto do jogador
  - Nome
  - Número de votos
  - Porcentagem
- Vencedor destacado (badge, coroa, etc.)

---

### 15. **Página: Configurações**

**Abas:**

#### Aba 1: Perfil do Usuário

Campos editáveis:
- Foto de perfil (upload)
- Nome de usuário
- Email
- Botão: "Salvar Alterações"

#### Aba 2: Segurança

Campos:
- Senha atual
- Nova senha
- Confirmar nova senha
- Botão: "Alterar Senha"

#### Aba 3: Preferências

Opções:
- Tema (Claro/Escuro)
- Idioma
- Notificações (checkboxes):
  - Email sobre próximas rodadas
  - Email sobre novos gols
  - Notificações push
- Botão: "Salvar Preferências"

---

## 🔄 Fluxos Principais de Uso

### Fluxo 1: Criar uma Nova Pelada e Jogar a Primeira Rodada

1. **Login** → Dashboard
2. **Minhas Peladas** → Clicar em "+ Nova Pelada"
3. Preencher formulário (Nome, Local, Dia, Horário) → Salvar
4. Ir para **Jogadores** → Adicionar jogadores da pelada
5. Ir para **Temporadas** → "+ Nova Temporada"
6. Preencher período (ex: Janeiro-Março 2025) → Criar
7. Entrar na temporada → Aba "Times Fixos"
8. **Criar Times** (ex: Time Azul, Time Vermelho)
9. Para cada time: **Gerenciar Jogadores** → Escalar jogadores
10. Aba "Rodadas" → "+ Nova Rodada"
11. Selecionar data, quantidade de times, jogadores por time → Criar
12. Entrar na rodada → "+ Criar Partida"
13. Selecionar Time Casa e Time Fora → Criar Partida
14. Entrar na partida → "Iniciar Partida"
15. Durante o jogo: "Registrar Gol" (jogador, minuto, assistência)
16. Ao fim: "Finalizar Partida" (atualiza pontos automaticamente)
17. Ver **Rankings** → Classificação atualizada

### Fluxo 2: Acompanhar Estatísticas de um Jogador

1. **Dashboard** → Menu **Jogadores**
2. Buscar ou filtrar jogador
3. Clicar no jogador → Ver detalhes
4. Visualizar:
   - Total de gols
   - Total de assistências
   - Times que já jogou
   - Histórico de partidas
   - Média de gols por jogo

### Fluxo 3: Ver Ranking da Temporada

1. **Dashboard** → Menu **Temporadas**
2. Selecionar temporada ativa
3. Aba "Ranking de Times"
4. Visualizar:
   - Classificação completa
   - Estatísticas de cada time
   - Artilheiros da temporada

### Fluxo 4: Criar e Gerenciar Times Fixos

1. **Temporadas** → Selecionar temporada
2. Aba "Times Fixos" → "+ Criar Time"
3. Nome do time, cor → Salvar
4. "Gerenciar Jogadores" → Selecionar jogadores disponíveis
5. Definir capitão e posições → Salvar
6. Times permanecem durante toda a temporada
7. Em cada rodada, apenas selecionar quais times jogam

---

## 📊 Componentes Reutilizáveis

### Cards
- Card de Estatística (número grande + ícone + label)
- Card de Pelada (info + ações)
- Card de Time (nome, cor, stats, botões)
- Card de Partida (placar, times, status)
- Card de Jogador (foto, nome, stats)

### Tabelas
- Tabela de Classificação (ranking de times)
- Tabela de Jogadores
- Tabela de Artilheiros
- Tabela de Assistências

### Modais
- Modal de Formulário (criar/editar)
- Modal de Confirmação (excluir)
- Modal de Detalhes

### Badges/Tags
- Status (Ativo, Inativo, Pendente, Finalizado)
- Resultados (Vitória, Empate, Derrota)
- Posições (Goleiro, Zagueiro, etc.)
- Capitão

### Botões
- Primário (CTA principal)
- Secundário (ações secundárias)
- Ícone (editar, excluir, visualizar)
- Link (navegação)

### Forms
- Input de texto
- Select/Dropdown
- Date picker
- Time picker
- Checkbox
- Radio button
- Upload de imagem
- Color picker

---

## 🎯 Interações e Estados

### Estados de Botões
- Default
- Hover
- Active
- Disabled
- Loading

### Estados de Partida
- **Agendada**: Cinza, aguardando início
- **Em andamento**: Verde, permite registrar gols
- **Finalizada**: Azul, somente visualização

### Estados de Temporada
- **Ativa**: Verde, pode criar rodadas e times
- **Encerrada**: Cinza, somente visualização

### Estados de Rodada
- **Pendente**: Aguardando data
- **Em andamento**: Partidas sendo jogadas
- **Finalizada**: Todas partidas concluídas

### Feedback Visual
- **Sucesso**: Toast verde (ex: "Time criado com sucesso!")
- **Erro**: Toast vermelho (ex: "Erro ao salvar partida")
- **Loading**: Spinner ou skeleton screens
- **Empty states**: Ilustração + texto quando não há dados

---

## 📱 Responsividade

### Desktop (>1024px)
- Sidebar fixa à esquerda
- Conteúdo em grid de 2-3 colunas
- Tabelas completas

### Tablet (768px - 1023px)
- Sidebar colapsável
- Conteúdo em 2 colunas
- Tabelas com scroll horizontal se necessário

### Mobile (<768px)
- Menu hamburguer
- Conteúdo em 1 coluna
- Cards empilhados verticalmente
- Tabelas transformadas em cards
- Modais em fullscreen

---

## 🔔 Notificações e Alertas

### Tipos de Notificação
1. **Nova rodada agendada** - "Rodada #5 agendada para 25/01/2025"
2. **Partida iniciada** - "Partida Time Azul x Time Vermelho iniciou!"
3. **Gol marcado** - "Goool! João Silva marcou para o Time Azul"
4. **Partida finalizada** - "Partida encerrada: Time Azul 3 x 2 Time Vermelho"
5. **Ranking atualizado** - "Time Azul assumiu a liderança!"

### Canais
- Notificações in-app (sino no header)
- Toast messages (canto da tela)
- Email (opcional, configurável)

---

## 🎮 Gamificação (Futuro)

Ideias para engajamento:
- **Badges/Conquistas**: Artilheiro da temporada, Hat-trick, Muralha (goleiro sem sofrer gols)
- **Níveis de jogador**: Rookie, Amador, Semi-pro, Profissional
- **Streak**: Sequência de vitórias
- **MVP da rodada**: Votação para melhor jogador

---

## 🔐 Permissões e Roles (Futuro)

### Organizador (Admin da Pelada)
- Criar/editar/excluir peladas
- Gerenciar jogadores
- Criar temporadas e rodadas
- Registrar partidas e gols
- Acesso total

### Jogador (Membro)
- Visualizar estatísticas
- Votar em enquetes
- Ver rankings e partidas
- Editar próprio perfil

---

## 📈 Métricas e Analytics (Futuro)

Dashboard de métricas:
- Peladas mais ativas
- Média de gols por rodada
- Time com mais vitórias
- Jogador com mais presenças
- Taxa de comparecimento por rodada

---

## 🛠️ Tecnologias Recomendadas para Frontend

### Framework/Biblioteca
- **React.js** + **TypeScript** (componentização, tipagem)
- **Next.js** (SSR, rotas, otimização)

### UI/Styling
- **Tailwind CSS** (utilitário, responsivo)
- **shadcn/ui** ou **Radix UI** (componentes acessíveis)
- **Lucide React** ou **React Icons** (ícones)

### Gerenciamento de Estado
- **Zustand** ou **Redux Toolkit** (global state)
- **React Query** (cache, fetching)

### Gráficos
- **Recharts** ou **Chart.js** (visualizações)

### Formulários
- **React Hook Form** + **Zod** (validação)

### Notificações
- **React Hot Toast** ou **Sonner**

---

## 📝 Observações Finais

### Prioridades para MVP (Primeira Versão)
1. ✅ Login/Registro
2. ✅ Dashboard básico
3. ✅ CRUD de Peladas
4. ✅ CRUD de Jogadores
5. ✅ Criar Temporada
6. ✅ Criar Times Fixos na Temporada
7. ✅ Escalar Jogadores nos Times
8. ✅ Criar Rodadas
9. ✅ Criar Partidas (selecionar times)
10. ✅ Registrar Gols
11. ✅ Finalizar Partida (atualizar pontos)
12. ✅ Ver Ranking de Times

### Features Secundárias (Versão 2)
- Votações
- Gráficos avançados
- Notificações em tempo real
- Exportar relatórios (PDF)
- Integração com Google Calendar
- Modo escuro

### Acessibilidade
- Navegação por teclado
- ARIA labels
- Contraste adequado (WCAG AA)
- Textos alternativos em imagens

---

**Documento criado para:** Geração de design UI/UX da plataforma EFootBool
**Versão:** 1.0
**Data:** 24/12/2025
