from __future__ import annotations

from uuid import uuid4

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .core.config import get_settings
from .db.database import (
    count_distinct_conversations,
    count_rows,
    initialize_database,
    list_recent_scripts,
    save_chat_message,
    save_generated_script,
)
from .models import ChatRequest, ChatResponse, DashboardSummary, HealthResponse, ScriptSummary
from .services.ai import generate_script

load_dotenv()

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description=settings.description,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event() -> None:
    initialize_database()


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        database_ready=True,
        ai_ready=bool(settings.openai_api_key),
    )


@app.post("/api/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    text = payload.message.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Envie uma mensagem para iniciar o chat.")

    conversation_id = payload.conversation_id or str(uuid4())
    save_chat_message(conversation_id, "user", text)

    generated = generate_script(text, payload.output_format)
    save_chat_message(conversation_id, "assistant", generated.reply)

    script_id = save_generated_script(
        conversation_id=conversation_id,
        question=text,
        output_format=payload.output_format,
        reply=generated.reply,
        script=generated.script,
        language=generated.language,
    )

    return ChatResponse(
        conversation_id=conversation_id,
        reply=generated.reply,
        script=generated.script,
        language=generated.language,
        output_format=payload.output_format,
        script_id=script_id,
    )


@app.get("/api/scripts", response_model=list[ScriptSummary])
def get_scripts() -> list[ScriptSummary]:
    rows = list_recent_scripts(limit=12)
    return [ScriptSummary(**row) for row in rows]


@app.get("/api/dashboard/summary", response_model=DashboardSummary)
def dashboard_summary() -> DashboardSummary:
    scripts_generated = count_rows("generated_scripts")
    active_users = count_distinct_conversations()
    recent_rows = list_recent_scripts(limit=3)

    return DashboardSummary(
        scripts_generated=scripts_generated,
        time_saved_hours=round(scripts_generated * 2.4, 1),
        success_rate=94 if scripts_generated else 0,
        active_users=active_users,
        recent_scripts=[ScriptSummary(**row) for row in recent_rows],
    )
