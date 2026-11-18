const configuredApiBase = process.env.NEXT_PUBLIC_API_BASE_URL?.trim();

export const API_BASE = (
  configuredApiBase || "http://127.0.0.1:8000"
).replace(/\/+$/, "");
