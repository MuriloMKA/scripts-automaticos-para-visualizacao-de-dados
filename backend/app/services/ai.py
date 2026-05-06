from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any
from uuid import uuid4

from ..core.config import get_settings


@dataclass(frozen=True)
class GeneratedScript:
    reply: str
    script: str
    language: str


SETTINGS = get_settings()


SYSTEM_PROMPT = """
Você é um assistente sênior de engenharia de dados SAP.
Responda sempre em português do Brasil.

Objetivo:
- Entender a necessidade de negócio.
- Gerar um script pronto para consumo em BI ou extração.
- Ser claro sobre premissas e limites.

Formato de resposta obrigatório em JSON válido com as chaves:
- reply: texto curto explicando o que foi gerado
- script: script pronto no formato solicitado
- language: sql | abap | json | powerquery
- notes: observações curtas

Se faltar contexto, faça uma suposição razoável e siga adiante.
""".strip()


def build_local_response(question: str, output_format: str) -> GeneratedScript:
    normalized_question = question.strip()
    format_key = output_format.lower()

    if format_key == "abap":
        language = "abap"
        script = (
            "@AbapCatalog.sqlViewName: 'ZSAP_SCRIPT'\n"
            "@EndUserText.label: 'Script SAP gerado automaticamente'\n"
            "define view Z_SAP_SCRIPT as select from mara {\n"
            "  key mara.matnr as Material,\n"
            "  mara.mtart as TipoMaterial\n"
            "}"
        )
        reply = "Gerei uma CDS View inicial em ABAP para você adaptar ao cenário SAP."
    elif format_key == "json":
        language = "json"
        script = json.dumps(
            {
                "question": normalized_question,
                "source": "SAP",
                "fields": ["Material", "Planta", "Quantidade"],
                "format": "json",
            },
            ensure_ascii=False,
            indent=2,
        )
        reply = "Estruturei a saída em JSON para facilitar integração com outras camadas."
    elif format_key == "powerbi":
        language = "powerquery"
        script = (
            "let\n"
            "    Source = Sap.Hana(\"sap-server:30015\"),\n"
            "    Data = Source{[Schema=\"SAPSR3\",Item=\"MARA\"]}[Data]\n"
            "in\n"
            "    Data"
        )
        reply = "Montei uma base simples em Power Query para conectar ao SAP."
    else:
        language = "sql"
        script = (
            "SELECT\n"
            "  MATNR AS material,\n"
            "  WERKS AS planta,\n"
            "  MENGE AS quantidade\n"
            "FROM MSEG\n"
            "WHERE BUDAT >= CURRENT_DATE - INTERVAL '90 DAY';"
        )
        reply = "Gerei um SQL base para iniciar a consulta SAP."

    if normalized_question:
        reply = f"{reply} Pergunta recebida: {normalized_question}"

    return GeneratedScript(reply=reply, script=script, language=language)


def generate_script(question: str, output_format: str) -> GeneratedScript:
    if not SETTINGS.openai_api_key:
        return build_local_response(question, output_format)

    payload: dict[str, Any] = {
        "model": SETTINGS.openai_model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Formato desejado: {output_format}\n"
                    f"Pergunta do usuário: {question}\n"
                    "Retorne JSON válido seguindo o formato pedido."
                ),
            },
        ],
        "temperature": 0.2,
    }

    request = urllib.request.Request(
        f"{SETTINGS.openai_base_url.rstrip('/')} /v1/chat/completions".replace(" ", ""),
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {SETTINGS.openai_api_key}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=SETTINGS.request_timeout_seconds) as response:
            response_payload = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, ValueError):
        return build_local_response(question, output_format)

    content = response_payload["choices"][0]["message"]["content"]
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        return build_local_response(question, output_format)

    reply = str(parsed.get("reply", "Resposta gerada pela IA."))
    script = str(parsed.get("script", ""))
    language = str(parsed.get("language", output_format)).lower()
    if not script.strip():
        script = build_local_response(question, output_format).script

    return GeneratedScript(reply=reply, script=script, language=language)
