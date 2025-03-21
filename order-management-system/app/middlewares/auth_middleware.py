from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from jwt_utils import verify_token

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in ["/login", "/refresh-token"]:  # Excluir rutas públicas
            return await call_next(request)

        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            raise HTTPException(status_code=403, detail="Not authorized")

        token = token.split(" ")[1]
        payload = verify_token(token)
        if not payload:
            raise HTTPException(status_code=403, detail="Invalid or expired token")

        request.state.user = payload  # Adjuntar usuario al request
        return await call_next(request)