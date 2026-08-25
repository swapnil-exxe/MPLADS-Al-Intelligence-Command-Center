import time
from typing import Dict, List, Tuple
from fastapi import Request, HTTPException, status

class RateLimiter:
    """
    In-memory leaky bucket rate limiter tracking requests by client IP.
    """
    def __init__(self):
        # Maps key (ip + endpoint_type) -> list of timestamp floats
        self._requests: Dict[str, List[float]] = {}

    def check_rate_limit(self, request: Request, endpoint_type: str, max_requests: int, window_seconds: int):
        client_ip = request.client.host if request.client else "127.0.0.1"
        # Handle X-Forwarded-For header if behind reverse proxy
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            client_ip = forwarded.split(",")[0].strip()

        key = f"{client_ip}:{endpoint_type}"
        now = time.time()
        cutoff = now - window_seconds

        # Clean old timestamps
        timestamps = self._requests.get(key, [])
        valid_timestamps = [t for t in timestamps if t > cutoff]

        if len(valid_timestamps) >= max_requests:
            retry_after = int(window_seconds - (now - valid_timestamps[0]))
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded for {endpoint_type}. Maximum {max_requests} requests per {window_seconds}s.",
                headers={"Retry-After": str(max(1, retry_after))}
            )

        valid_timestamps.append(now)
        self._requests[key] = valid_timestamps

limiter = RateLimiter()
