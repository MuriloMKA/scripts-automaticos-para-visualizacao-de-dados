from __future__ import annotations

import base64
import json
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any

from ..core.config import get_settings


@dataclass(frozen=True)
class SapConnectionInfo:
    provider: str
    base_url: str | None
    ready: bool
    message: str


SETTINGS = get_settings()


def _build_basic_auth_header(username: str, password: str) -> str:
    token = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")
    return f"Basic {token}"


def get_connection_info() -> SapConnectionInfo:
    provider = (getattr(SETTINGS, "sap_connector_type", "odata") or "odata").lower()
    base_url = getattr(SETTINGS, "sap_odata_base_url", "") or None
    username = getattr(SETTINGS, "sap_odata_username", "")
    password = getattr(SETTINGS, "sap_odata_password", "")

    if provider != "odata":
        return SapConnectionInfo(
            provider=provider,
            base_url=base_url,
            ready=False,
            message="Conector SAP configurado para um provider ainda nao implementado neste projeto.",
        )

    if not base_url:
        return SapConnectionInfo(
            provider=provider,
            base_url=None,
            ready=False,
            message="SAP OData ainda nao configurado. Defina SAP_ODATA_BASE_URL no .env.",
        )

    if not username or not password:
        return SapConnectionInfo(
            provider=provider,
            base_url=base_url,
            ready=False,
            message="Credenciais SAP OData ausentes. Defina SAP_ODATA_USERNAME e SAP_ODATA_PASSWORD.",
        )

    return SapConnectionInfo(
        provider=provider,
        base_url=base_url,
        ready=True,
        message="SAP OData configurado e pronto para consultas de leitura.",
    )


def health_check() -> SapConnectionInfo:
    info = get_connection_info()
    if not info.ready or not info.base_url:
        return info

    ping_url = info.base_url.rstrip("/")
    request = urllib.request.Request(
        ping_url,
        headers={
            "Accept": "application/json",
            "Authorization": _build_basic_auth_header(
                getattr(SETTINGS, "sap_odata_username", ""),
                getattr(SETTINGS, "sap_odata_password", ""),
            ),
        },
        method="GET",
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            status_ok = 200 <= int(response.status) < 400
    except (urllib.error.URLError, TimeoutError, ValueError):
        return SapConnectionInfo(
            provider=info.provider,
            base_url=info.base_url,
            ready=False,
            message="SAP OData configurado, mas o endpoint nao respondeu ao teste de conexao.",
        )

    return SapConnectionInfo(
        provider=info.provider,
        base_url=info.base_url,
        ready=status_ok,
        message="SAP OData respondeu ao teste de conexao com sucesso.",
    )


def preview_odata_entity(entity_path: str, top: int = 50, select: list[str] | None = None) -> dict[str, Any]:
    info = get_connection_info()
    
    # If SAP is not ready, use mock data for demonstration
    if not info.ready or not info.base_url:
        from . import mock_sap
        payload = mock_sap.get_mock_odata_response(entity_path, top, select)
        results = payload.get("d", {}).get("results", [])
        return {
            "entity_path": entity_path,
            "count": len(results),
            "rows": results,
            "source_url": "[MOCK DATA - SAP not configured]",
        }

    query: dict[str, str] = {
        "$top": str(top),
        "$format": "json",
    }
    if select:
        query["$select"] = ",".join(select)

    url = f"{info.base_url.rstrip('/')}/{entity_path.lstrip('/')}?{urllib.parse.urlencode(query)}"

    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "Authorization": _build_basic_auth_header(
                getattr(SETTINGS, "sap_odata_username", ""),
                getattr(SETTINGS, "sap_odata_password", ""),
            ),
        },
        method="GET",
    )

    with urllib.request.urlopen(request, timeout=SETTINGS.request_timeout_seconds) as response:
        payload = json.loads(response.read().decode("utf-8"))

    results = (
        payload.get("d", {}).get("results")
        if isinstance(payload, dict)
        else []
    )
    if not isinstance(results, list):
        results = []

    return {
        "entity_path": entity_path,
        "count": len(results),
        "rows": results,
        "source_url": url,
    }
