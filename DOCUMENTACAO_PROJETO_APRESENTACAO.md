# Documentacao do Projeto - SAP Script AI

## 1. Visao Geral

O projeto `scripts-automaticos-para-visualizacao-de-dados` e uma plataforma para transformar perguntas de negocio em scripts tecnicos (SQL, ABAP CDS, JSON e Power Query) usando IA.

### Objetivo principal

- Reduzir dependencia tecnica de analistas de negocio para extrair dados SAP.
- Acelerar criacao de consultas e datasets para Power BI.
- Manter historico dos scripts gerados para auditoria e reaproveitamento.

### Stack atual

- Frontend: React + Vite + TypeScript
- Backend: FastAPI (Python)
- Banco: SQLite (arquivo local)
- IA: endpoint OpenAI-compatible (com fallback local)
- Auth: JWT + hash de senha (bcrypt/passlib)

---

## 2. Arquitetura Atual

## 2.1 Camadas

1. Interface (Frontend)

- Telas de Dashboard, Chat e Analytics.
- Consome a API via `/api/*`.
- No ambiente dev, o Vite faz proxy para `http://127.0.0.1:8000`.

2. API (Backend FastAPI)

- Expõe endpoints de chat, scripts, dashboard e autenticacao.
- Valida payloads com Pydantic.
- Aplica CORS configuravel.

3. Persistencia (SQLite)

- Guarda mensagens de chat, scripts gerados e usuarios.
- Cria tabelas automaticamente no startup.

4. Servico de IA

- Se `OPENAI_API_KEY` estiver configurada, chama provedor real.
- Se nao estiver, gera fallback local para manter o fluxo funcional.

## 2.2 Fluxo principal (Chat)

1. Usuario envia pergunta no frontend.
2. Front chama `POST /api/chat` com `message`, `output_format` e `conversation_id`.
3. Backend salva mensagem do usuario em `chat_messages`.
4. Backend chama servico de IA (`generate_script`).
5. Backend salva resposta e script em `generated_scripts`.
6. Front recebe `reply + script + language` e renderiza no chat.

---

## 3. Backend - Como esta funcionando hoje

## 3.1 Inicializacao

Arquivo principal: `backend/app/main.py`

No startup:

- `initialize_database()` cria/atualiza tabelas.
- `ensure_default_user()` garante usuario admin padrao.

Admin padrao:

- Email: `admin@klabin.com.br`
- Senha: `admin`

## 3.2 Endpoints disponiveis

1. `GET /health`

- Retorna status da API, disponibilidade do banco e se a IA real esta ativa.

2. `POST /api/auth/register`

- Cria usuario no banco.
- Salva senha com hash (`bcrypt`).

3. `POST /api/auth/login`

- Valida credenciais.
- Retorna `access_token` JWT + dados do usuario.

4. `POST /api/chat`

- Recebe pergunta + formato desejado.
- Gera script via IA (real ou fallback).
- Persiste historico.

5. `GET /api/scripts`

- Lista scripts recentes globais.

6. `GET /api/scripts/user/{user_id}`

- Lista scripts de um usuario especifico.

7. `GET /api/dashboard/summary`

- Exige token JWT.
- Retorna metricas agregadas para dashboard.

## 3.3 Banco de dados (SQLite)

Arquivo: `backend/data/app.db`

Tabelas:

- `users`
  - `id`, `email`, `hashed_password`, `full_name`, `role`, `created_at`

- `chat_messages`
  - `id`, `conversation_id`, `role`, `content`, `created_at`

- `generated_scripts`
  - `id`, `user_id`, `conversation_id`, `question`, `output_format`, `reply`, `script`, `language`, `created_at`

Indices:

- Conversas por `conversation_id`
- Scripts recentes por `created_at`

## 3.4 Seguranca atual

- Senhas hash com passlib+bcrypt.
- JWT para rotas protegidas.
- Chave JWT agora e configuravel por ambiente.

Variaveis obrigatorias de auth:

- `JWT_SECRET_KEY`
- `JWT_ALGORITHM`
- `JWT_EXPIRE_MINUTES`

---

## 4. Integracao IA - Estado Atual

## 4.1 O que ja funciona

- Prompt de sistema estruturado para engenharia de dados SAP.
- Suporte a formatos: `sql`, `abap`, `json`, `powerbi`.
- Fallback local robusto para continuidade sem API key.

## 4.2 O que falta para IA em nivel producao

1. Prompt engineering por dominio

- Criar prompts por area (vendas, estoque, financeiro, fiscal).

2. Guardrails de geracao

- Validar SQL/ABAP antes de retornar ao usuario.
- Bloquear comandos perigosos (`DROP`, `DELETE` sem contexto).

3. Observabilidade

- Log estruturado de latencia, erros e custo de tokens.
- Tracking de taxa de sucesso por tipo de consulta.

4. Controle de custo

- Cache de respostas repetidas.
- Limites por usuario e por dia.

5. Qualidade

- Suite de testes com perguntas reais da operacao.
- Benchmark de acuracia por dominio SAP.

---

## 5. O que falta para integrar com banco SAP real

Hoje o projeto ainda NAO consulta SAP diretamente. A geracao de scripts existe, mas a execucao contra SAP ainda nao foi implementada.

## 5.1 Passos para integrar SAP em etapas

### Etapa 1 - Escolha tecnica de conectividade

Escolher uma opcao:

- SAP HANA (ODBC/JDBC)
- SAP RFC/BAPI
- SAP OData
- Extracao para Data Lake/SQL intermediario

### Etapa 2 - Modulo de conexao

Criar camada `app/services/sap_client.py` com:

- gestao de conexao
- timeout
- retries
- tratamento de erro e auditoria

### Etapa 3 - Credenciais seguras

Adicionar no `.env`:

- `SAP_HOST`, `SAP_PORT`, `SAP_CLIENT`, `SAP_USER`, `SAP_PASSWORD`
- Nunca commitar credenciais reais

### Etapa 4 - Endpoint de validacao SAP

Exemplo:

- `GET /api/sap/health`
- testa autenticacao e permissao basica no SAP

### Etapa 5 - Execucao controlada de query

Criar endpoint:

- `POST /api/sap/query/preview`
- executa apenas leitura + limite de linhas
- audita usuario, tempo e consulta executada

### Etapa 6 - Mapeamento semantico de tabelas

Criar catalogo de dados SAP por dominio:

- tabelas chave
- relacionamentos
- campos sensiveis
- regras de governanca

### Etapa 7 - RLS e governanca

- Row-level security por perfil
- mascaramento de colunas sensiveis
- trilha de auditoria completa

---

## 6. Integracao Frontend com dados reais

## 6.1 O que ja esta integrado

- Chat usando `POST /api/chat`
- Dashboard/Analytics consumindo `GET /api/dashboard/summary`
- Lista de scripts consumindo `GET /api/scripts`

## 6.2 O que ainda falta no front

1. Fluxo completo de autenticacao

- Login/registro conectados ao backend com armazenamento seguro do token.
- Envio do token `Authorization: Bearer <token>` nas rotas protegidas.

2. Controle de sessao

- Logout, expiracao de token e refresh strategy.

3. UX de erros

- mensagens claras para 401/403/500.
- estado de loading e retry.

4. Telas de historico por usuario

- consumir `/api/scripts/user/{user_id}`.

---

## 7. Riscos e decisoes de arquitetura

## 7.1 Riscos atuais

- SQLite nao e ideal para alta concorrencia em producao.
- Sem integracao SAP real ainda nao existe leitura de dados operacionais.
- Prompt unico pode gerar variabilidade alta por dominio.

## 7.2 Evolucao recomendada

1. Trocar SQLite por PostgreSQL em ambiente produtivo.
2. Adicionar migrations (Alembic) para versionar schema.
3. Introduzir fila assicrona para operacoes de IA demoradas.
4. Observabilidade (logs estruturados + metricas + tracing).

---

## 8. Roadmap sugerido (curto prazo)

Sprint 1 (concluido/parcial)

- Backend com auth, chat, scripts e dashboard.
- Persistencia local com SQLite.
- Integracao frontend com endpoints reais.

Sprint 2

- Integracao SAP (health + preview query).
- Catalogo de tabelas por dominio.
- Validacao de query antes da execucao.

Sprint 3

- Historico por usuario no front.
- Controle de permissoes por role.
- Dashboard com metricas reais por usuario.

Sprint 4

- Hardening de seguranca.
- Deploy e monitoracao.
- Testes E2E e testes de carga.

---

## 9. Como demonstrar na apresentacao

Roteiro de demo (5-8 minutos):

1. Mostrar login e token JWT.
2. Mostrar chat recebendo pergunta de negocio.
3. Mostrar script gerado em formato selecionado (SQL/ABAP/JSON/Power Query).
4. Mostrar persistencia no dashboard (scripts e metricas atualizadas).
5. Explicar fallback local vs IA real.
6. Encerrar com roadmap SAP real (etapas 1-7).

---

## 10. Comandos uteis

Backend:

```bash
cd backend
c:/Users/Muril/OneDrive/Desktop/scripts-automaticos-para-visualizacao-de-dados/.venv/Scripts/python.exe -m pip install -r requirements.txt
c:/Users/Muril/OneDrive/Desktop/scripts-automaticos-para-visualizacao-de-dados/.venv/Scripts/python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Health checks:

- Backend: `http://127.0.0.1:8000/health`
- Swagger: `http://127.0.0.1:8000/docs`

---

## 11. Resumo executivo

O projeto ja saiu do modo mock simples e hoje possui:

- camada de API com autenticacao,
- persistencia local,
- geracao de script com IA/fallback,
- e consumo real no frontend.

O proximo marco tecnico para virar produto de dados corporativo e a integracao controlada com SAP real (conector + governanca + validacao de query + seguranca por perfil).
