export type OutputFormat = "sql" | "abap" | "json" | "powerbi";

export type ScriptSummary = {
  id: number;
  question: string;
  output_format: OutputFormat;
  reply: string;
  script: string;
  language: string;
  created_at: string;
};

export type ChatResponse = {
  conversation_id: string;
  reply: string;
  script: string;
  language: string;
  output_format: OutputFormat;
  script_id: number;
};

export type DashboardSummary = {
  scripts_generated: number;
  time_saved_hours: number;
  success_rate: number;
  active_users: number;
  recent_scripts: ScriptSummary[];
};

async function requestJson<T>(
  url: string,
  init?: RequestInit
): Promise<T> {
  const token = localStorage.getItem("token");

  const headers = {
    ...init?.headers,
    "Content-Type": "application/json",
    ...(token
      ? { Authorization: `Bearer ${token}` }
      : {}),
  };

  const response = await fetch(url, {
    ...init,
    headers,
  });

  if (response.status === 401) {
    localStorage.clear();
    window.location.href = "/login";
    throw new Error("Unauthorized");
  }

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export function sendChatMessage(payload: {
  message: string;
  output_format: OutputFormat;
  conversation_id?: string | null;
}): Promise<ChatResponse> {
  return requestJson<ChatResponse>("/api/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
}

export function fetchDashboardSummary(): Promise<DashboardSummary> {
  return requestJson<DashboardSummary>("/api/dashboard/summary");
}

export function fetchRecentScripts(): Promise<ScriptSummary[]> {
  return requestJson<ScriptSummary[]>("/api/scripts");
}

export const authApi = {
  login: (p: any) =>
    requestJson<{
      access_token: string;
      token_type: string;
      user: any;
    }>("/api/auth/login", {
      method: "POST",
      body: JSON.stringify(p),
    }),
};