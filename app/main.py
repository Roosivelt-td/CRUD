from fastapi import FastAPI
from app.database import engine, Base, SessionLocal
from app.models.product import ProductModel
from app.models.order import OrderModel
from app.models.user import UserModel
from app.controllers.auth_controller import router as auth_router, get_password_hash
from app.controllers.store_controller import router as store_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Tienda Online - MVC con Autenticación y Roles")

# Seed default admin user on startup
def create_default_admin():
    db = SessionLocal()
    try:
        admin_email = "admin@tienda.com"
        existing_admin = db.query(UserModel).filter(UserModel.email == admin_email).first()
        if not existing_admin:
            default_admin = UserModel(
                username="Administrador",
                email=admin_email,
                password_hash=get_password_hash("admin123"),
                role="admin"
            )
            db.add(default_admin)
            db.commit()
    finally:
        db.close()

create_default_admin()

# Include routers
app.include_router(auth_router)
app.include_router(store_router)
