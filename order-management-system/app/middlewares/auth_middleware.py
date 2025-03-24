from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from .jwt_utils import verify_token

class AuthMiddleware(BaseHTTPMiddleware):
    # Lista de rutas protegidas que requieren validación
    protected_routes = []

    async def dispatch(self, request: Request, call_next):
        # Verifica si la ruta actual está en la lista de rutas protegidas
        if any(request.url.path.startswith(route) for route in self.protected_routes):
            token = request.headers.get("Authorization")
            if not token or not token.startswith("Bearer "):
                raise HTTPException(status_code=403, detail="Not authorized")

            token = token.split(" ")[1]
            payload = verify_token(token)
            if not payload:
                raise HTTPException(status_code=403, detail="Invalid or expired token")

            request.state.user = payload  # Adjuntar usuario al request

        # Si la ruta no está protegida, continúa sin validación
        return await call_next(request)