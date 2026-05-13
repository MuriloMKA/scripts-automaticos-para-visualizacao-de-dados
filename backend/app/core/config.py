from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv


_ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(_ENV_PATH)


@dataclass(frozen=True)
class Settings:
    app_name: str = "API - Visualizacao de Dados SAP"
    version: str = "0.2.0"
    description: str = "Backend com IA e SQLite para scripts SAP."
    host: str = "127.0.0.1"
    port: int = 8000
    cors_origins: List[str] = None  # type: ignore[assignment]
    database_path: Path = Path(__file__).resolve().parents[2] / "data" / "app.db"
    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com"
    openai_model: str = "gpt-4o-mini"
    request_timeout_seconds: int = 60
    jwt_secret_key: str = "CHANGE_ME_IN_ENV"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 480
    sap_connector_type: str = "odata"
    sap_odata_base_url: str = ""
    sap_odata_username: str = ""
    sap_odata_password: str = ""

    def __post_init__(self) -> None:
        if self.cors_origins is None:
            object.__setattr__(self, "cors_origins", [
                "http://localhost:5173",
                "http://127.0.0.1:5173",
                "http://localhost:4173",
                "http://127.0.0.1:4173",
            ])


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    cors_origins_env = os.getenv("CORS_ORIGINS", "")
    cors_origins = [origin.strip() for origin in cors_origins_env.split(",") if origin.strip()]

    settings = Settings(
        app_name=os.getenv("APP_NAME", "API - Visualizacao de Dados SAP"),
        version=os.getenv("APP_VERSION", "0.2.0"),
        description=os.getenv("APP_DESCRIPTION", "Backend com IA e SQLite para scripts SAP."),
        host=os.getenv("BACKEND_HOST", "127.0.0.1"),
        port=int(os.getenv("BACKEND_PORT", "8000")),
        cors_origins=cors_origins or None,
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        openai_base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com"),
        openai_model=os.getenv("MODEL_NAME", "gpt-4o-mini"),
        request_timeout_seconds=int(os.getenv("REQUEST_TIMEOUT_SECONDS", "60")),
        jwt_secret_key=os.getenv("JWT_SECRET_KEY", "CHANGE_ME_IN_ENV"),
        jwt_algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
        jwt_expire_minutes=int(os.getenv("JWT_EXPIRE_MINUTES", "480")),
        sap_connector_type=os.getenv("SAP_CONNECTOR_TYPE", "odata"),
        sap_odata_base_url=os.getenv("SAP_ODATA_BASE_URL", ""),
        sap_odata_username=os.getenv("SAP_ODATA_USERNAME", ""),
        sap_odata_password=os.getenv("SAP_ODATA_PASSWORD", ""),
    )
    return settings
