from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field

OutputFormat = Literal["sql", "abap", "json", "powerbi"]


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, description="Pergunta do usuário em linguagem natural.")
    output_format: OutputFormat = Field(default="sql", description="Formato do script desejado.")
    conversation_id: Optional[str] = Field(default=None, description="Identificador da conversa.")


class ChatResponse(BaseModel):
    conversation_id: str
    reply: str
    script: str
    language: str
    output_format: OutputFormat
    script_id: int


class ScriptSummary(BaseModel):
    id: int
    question: str
    output_format: OutputFormat
    reply: str
    script: str
    language: str
    created_at: datetime


class ConversationMessage(BaseModel):
    id: int
    conversation_id: str
    role: Literal["user", "assistant"]
    content: str
    created_at: datetime


class HealthResponse(BaseModel):
    status: str
    database_ready: bool
    ai_ready: bool


class DashboardSummary(BaseModel):
    scripts_generated: int
    time_saved_hours: float
    success_rate: int
    active_users: int
    recent_scripts: list[ScriptSummary]

class RegisterRequest(BaseModel):
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)
    full_name: str = Field(min_length=1)


class LoginRequest(BaseModel):
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)