# Roteiro de Slides - Apresentacao da Banca

## Slide 1 - Capa

- Titulo: SAP Script AI
- Subtitulo: Criacao automatizada de scripts para visualizacao de dados SAP
- Integrantes, curso, disciplina, data

## Slide 2 - Contexto e problema

- Dificuldade de traduzir perguntas de negocio em consultas SAP
- Dependencia de especialistas tecnicos
- Impacto em tempo, autonomia e tomada de decisao

## Slide 3 - Objetivo do projeto

- Gerar scripts tecnicos a partir de linguagem natural
- Suportar multiplos formatos (SQL, ABAP, JSON, Power Query)
- Persistir historico e indicadores de uso

## Slide 4 - Solucao proposta

- Interface de chat para perguntas de negocio
- Backend com IA para geracao de scripts
- Banco para historico e metricas

## Slide 5 - Arquitetura

- Frontend React
- Backend FastAPI
- Banco SQLite
- Servico de IA (OpenAI-compatible + fallback)
- Fluxo: usuario -> API -> IA -> banco -> dashboard

## Slide 6 - Backend em funcionamento

- Endpoints de auth, chat, scripts e dashboard
- JWT para seguranca
- Criacao automatica de tabelas
- Usuario admin default para bootstrap

## Slide 7 - Banco de dados

- Tabela users
- Tabela chat_messages
- Tabela generated_scripts
- Exemplo de rastreabilidade: quem perguntou, o que foi gerado, quando

## Slide 8 - IA e geracao de queries

- Prompt orientado para SAP
- Formatos de saida suportados
- Fallback local sem chave para continuidade
- Cenario atual: ambiente sem chave real, mas fluxo operacional

## Slide 9 - Demo (ao vivo)

- Login
- Envio de pergunta no chat
- Script gerado
- Registro no banco
- Dashboard atualizado

## Slide 10 - Resultados parciais

- Fluxo ponta a ponta operacional
- Persistencia e monitoramento basico
- Base pronta para escalar integracao SAP real

## Slide 11 - Gaps e riscos

- Sem conector SAP real no momento
- SQLite nao e banco de producao para alta concorrencia
- Necessidade de governanca para execucao segura de queries

## Slide 12 - Roadmap tecnico

- Sprint 1: conector SAP + health SAP
- Sprint 2: preview seguro de query + catalogo de tabelas
- Sprint 3: RBAC e auditoria avancada
- Sprint 4: migracao para PostgreSQL + observabilidade

## Slide 13 - Conclusao

- Projeto ja entrega valor academico e tecnico
- Demonstra viabilidade de IA aplicada ao contexto SAP
- Proximo passo e a conexao direta com dados SAP corporativos

## Slide 14 - Perguntas

- Abertura para duvidas da banca
