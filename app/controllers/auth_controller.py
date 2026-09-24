from fastapi import APIRouter, Depends, Request, Form, HTTPException, status, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import Optional

from app.database import get_db
from app.models.user import UserModel

router = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_current_user(request: Request, db: Session = Depends(get_db)):
    user_email = request.cookies.get("user_email")
    if not user_email:
        return None
    return db.query(UserModel).filter(UserModel.email == user_email).first()

@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})

@router.post("/login")
def login(
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        return templates.TemplateResponse("login.html", {
            "request": {},
            "error": "Correo o contraseña incorrectos."
        })

    # Set cookies for session
    resp = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    resp.set_cookie(key="user_email", value=user.email)
    resp.set_cookie(key="user_role", value=user.role)
    resp.set_cookie(key="username", value=user.username)
    return resp

@router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "error": None})

@router.post("/register")
def register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    existing_user = db.query(UserModel).filter(UserModel.email == email).first()
    if existing_user:
        return templates.TemplateResponse("register.html", {
            "request": {},
            "error": "El correo ya está registrado."
        })

    hashed_pwd = get_password_hash(password)
    new_user = UserModel(
        username=username,
        email=email,
        password_hash=hashed_pwd,
        role="user"
    )
    db.add(new_user)
    db.commit()

    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/logout")
def logout():
    resp = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    resp.delete_cookie("user_email")
    resp.delete_cookie("user_role")
    resp.delete_cookie("username")
    return resp
