const API_BASE = (import.meta.env.VITE_API_BASE_URL as string | undefined) ?? "/api";

let csrfLoaded = false;

function getCsrfToken(): string | null {
  const match = document.cookie
    .split("; ")
    .find((row) => row.startsWith("csrftoken="));
  return match ? decodeURIComponent(match.split("=")[1]) : null;
}

async function ensureCsrfCookie(): Promise<void> {
  if (csrfLoaded) {
    return;
  }

  try {
    await fetch(`${API_BASE}/auth/csrf`, {
      method: "GET",
      credentials: "include",
    });
  } finally {
    csrfLoaded = true;
  }
}

async function parseResponse<T>(response: Response): Promise<T> {
  const contentType = response.headers.get("content-type") ?? "";
  const isJson = contentType.includes("application/json");

  if (!response.ok) {
    if (isJson) {
      const errorPayload = (await response.json()) as Record<string, unknown>;
      const detail = (errorPayload.detail as string | undefined) ?? (errorPayload.message as string | undefined) ?? `Request failed with status ${response.status}`;
      throw new Error(detail);
    }
    throw new Error(`Request failed with status ${response.status}`);
  }

  if (response.status === 204) {
    return {} as T;
  }

  if (!isJson) {
    return {} as T;
  }

  return (await response.json()) as T;
}

export async function apiRequest<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const method = options.method?.toUpperCase() ?? "GET";
  const needsCsrf = method !== "GET" && method !== "HEAD" && method !== "OPTIONS";

  if (needsCsrf) {
    await ensureCsrfCookie();
  }

  const headers = new Headers(options.headers ?? {});

  if (!headers.has("Content-Type") && options.body && !(options.body instanceof FormData)) {
    headers.set("Content-Type", "application/json");
  }

  if (needsCsrf) {
    const token = getCsrfToken();
    if (token) {
      headers.set("X-CSRFToken", token);
    }
  }

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
    credentials: "include",
  });

  return parseResponse<T>(response);
}
