from fastapi import FastAPI
from app.routes.order_routes import router as order_router
from app.routes.item_routes import router as item_router
from app.routes.user_routes import router as user_router
from app.routes.employee_routes import router as employee_router
from app.routes.auth_routes import router as auth_router
from app.middlewares.auth_middleware import AuthMiddleware
from app.database.database import initialize_database

app = FastAPI()

initialize_database()

# Add authentication middleware
app.add_middleware(AuthMiddleware)

# Include all routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(order_router, prefix="/orders", tags=["Orders"])
app.include_router(item_router, prefix="/items", tags=["Items"])
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(employee_router, prefix="/employees", tags=["Employees"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Order Management System"}