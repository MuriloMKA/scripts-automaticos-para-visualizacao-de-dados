# Integração Real com SAP (Backend)

## 1. O que já foi preparado

O backend agora possui uma camada de integração SAP via **OData REST** com:

- verificação de status da conexão SAP
- preview de entidades SAP em modo somente leitura
- proteção por JWT nas rotas SAP
- fallback para continuar o projeto mesmo sem SAP configurado

Arquivos principais:

- `backend/app/services/sap.py`
- `backend/app/main.py`
- `backend/app/core/config.py`
- `backend/app/models.py`

---

## 2. O que você precisa para usar SAP de verdade

Para conectar em um ambiente SAP OData real, você precisa destes dados:

- `SAP_ODATA_BASE_URL`
- `SAP_ODATA_USERNAME`
- `SAP_ODATA_PASSWORD`
- `SAP_CONNECTOR_TYPE=odata`

### Exemplo de base URL

Pode variar conforme o ambiente SAP, mas normalmente segue um destes formatos:

- `http://seu-servidor:8000/sap/opu/odata/sap/SEU_SERVICO/`
- `https://seu-servidor/sap/opu/odata/sap/SEU_SERVICO/`

O caminho exato depende do serviço exposto no SAP Gateway.

---

## 3. Como configurar o `.env`

No arquivo `backend/.env`, adicione:

```env
SAP_CONNECTOR_TYPE=odata
SAP_ODATA_BASE_URL=https://seu-servidor/sap/opu/odata/sap/SEU_SERVICO/
SAP_ODATA_USERNAME=seu_usuario
SAP_ODATA_PASSWORD=sua_senha
```

---

## 4. Como testar se a conexão SAP está viva

### Via backend

```bash
GET /api/sap/health
```

### Resposta esperada

- `ready: true`
- `provider: odata`
- `message`: conexão válida

Se não estiver configurado:

- `ready: false`
- mensagem explicando o que falta

---

## 5. Como testar uma entidade SAP

Use o endpoint:

```bash
POST /api/sap/query/preview
```

Exemplo de payload:

```json
{
  "entity_path": "sap/opu/odata/sap/SEU_SERVICO/EntitySet",
  "top": 10,
  "select": ["Field1", "Field2"]
}
```

### Observação

- Esse endpoint é de leitura.
- Ele faz apenas preview dos dados retornados pela entidade OData.

---

## 6. Como a IA entra nessa etapa

Hoje a IA já gera scripts no backend, mas o próximo passo é deixá-la mais inteligente com contexto SAP real.

Fluxo ideal:

1. Usuário pergunta algo em linguagem natural.
2. Backend consulta o catálogo SAP ou uma entidade OData de apoio.
3. A IA recebe contexto de tabelas/campos/regras.
4. A resposta é gerada com mais precisão.

---

## 7. Limitações atuais

A integração real está pronta para **SAP OData**.

Ainda não foi implementado neste projeto:

- SAP HANA via driver direto
- RFC/BAPI
- extração ABAP nativa

Se o seu SAP usar outro tipo de integração, a estrutura atual pode ser adaptada com um novo conector.

---

## 8. Próximo passo recomendado

Depois de preencher o `.env` com os dados reais do SAP:

1. Reinicie o backend
2. Teste `GET /api/sap/health`
3. Teste `POST /api/sap/query/preview`
4. Conecte a UI do frontend nesses endpoints
5. Ajuste o prompt da IA com os metadados SAP retornados

---

## 9. Resumo curto

O projeto já está preparado para falar com SAP de verdade via OData. Falta apenas informar a URL do serviço, usuário e senha do ambiente SAP e apontar a entidade que você quer consultar.
