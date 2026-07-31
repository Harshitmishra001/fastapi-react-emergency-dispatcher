from fastapi import HTTPException, Request, status
import time
from collections import defaultdict

from backend.config.settings import settings

# In-memory store for rate limiting (IP -> [timestamps])
# In production, this would be Redis.
_request_history = defaultdict(list)

async def check_rate_limit(request: Request):
    """
    FastAPI dependency to enforce rate limits per IP.
    """
    client_ip = request.client.host if request.client else "unknown"
    now = time.time()
    
    # Clean up timestamps older than 60 seconds
    _request_history[client_ip] = [t for t in _request_history[client_ip] if now - t < 60]
    
    if len(_request_history[client_ip]) >= settings.RATE_LIMIT_PER_MINUTE:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Try again later."
        )
        
    _request_history[client_ip].append(now)
    return True
