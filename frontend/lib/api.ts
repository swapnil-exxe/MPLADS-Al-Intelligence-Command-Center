export const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || '';

export async function apiFetch(endpoint: string, options: RequestInit = {}) {
  const headers = new Headers(options.headers || {});
  headers.set('ngrok-skip-browser-warning', 'true');
  headers.set('Bypass-Tunnel-Remainder', 'true');

  const fullUrl = endpoint.startsWith('http') ? endpoint : `${API_BASE}${endpoint}`;
  return fetch(fullUrl, {
    ...options,
    headers,
  });
}
