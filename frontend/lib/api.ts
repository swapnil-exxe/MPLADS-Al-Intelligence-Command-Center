const DEFAULT_PUBLIC_BACKEND = 'https://c490ebb817030f.lhr.life';
const LOCAL_BACKEND = 'http://localhost:8001';

export const getApiBase = (): string => {
  if (process.env.NEXT_PUBLIC_API_BASE_URL) {
    return process.env.NEXT_PUBLIC_API_BASE_URL;
  }
  if (typeof window !== 'undefined') {
    const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
    return isLocalhost ? LOCAL_BACKEND : DEFAULT_PUBLIC_BACKEND;
  }
  return LOCAL_BACKEND;
};

export const API_BASE = getApiBase();
